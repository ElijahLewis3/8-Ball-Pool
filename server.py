import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData          # this should be replace with multipart in the future
import os;
import glob;
import Physics;
import math;
import random;
import json

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0";"/>""";

GAME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{game_name} - Billiards</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<h1 class="title">Billiards</h1>
<div class="divider"></div>
<div class="game-header">
    <div class="player-badge active" data-player="{player1_name}"><span class="label">Player 1</span> <span class="name">{player1_name}</span></div>
    <div class="player-badge" data-player="{player2_name}"><span class="label">Player 2</span> <span class="name">{player2_name}</span></div>
</div>
<p id="game-status">Drag the cue ball to shoot</p>
<div class="container" id="svg-container"></div>

<script src="script.js"></script>
</body>
</html>"""

# player1_name = ""
# player2_name = ""
# game_name = ""

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    session_data = {}

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/homepage.html', '/index.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        elif parsed.path.endswith('.svg') and parsed.path.startswith('/table-'):
            # Dynamically handle SVG files without hardcoding the file name
            try:
                with open('.' + parsed.path, 'rb') as fp:  # Open the file in binary mode
                    content = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")  # Set the correct content type for SVG files
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            except IOError:
                # File not found, return 404
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("404: File not found %s" % parsed.path, "utf-8"))

        elif parsed.path == '/script.js':
            with open('script.js', 'rb') as fp:
                content = fp.read()

            # Send a 200 OK response with the JavaScript content
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)

        elif parsed.path == '/styles.css':
            with open('styles.css', 'rb') as fp:
                content = fp.read()

            # Send a 200 OK response with the JavaScript content
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)


        # check if the web-pages matches the list

        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed = urlparse(self.path)
        
        # Define variables outside of the conditions
        player1_name = None
        player2_name = None
        game_name = None

        if self.path == "/start_game":
            # Parse form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # Extract player and game information from form data
            player1_name = form.getvalue('player1_name')
            player2_name = form.getvalue('player2_name')
            game_name = form.getvalue('game_name')
            # Store player and game names in session data
            self.session_data['player1_name'] = player1_name
            self.session_data['player2_name'] = player2_name
            self.session_data['game_name'] = game_name

            # Reset database and initialize game state for a new game
            if os.path.exists('phylib.db'):
                os.remove('phylib.db')

            self.session_data['table'] = createNewTable()
            self.session_data['game'] = Physics.Game(
                gameName=game_name,
                player1Name=player1_name,
                player2Name=player2_name
            )
            self.session_data['current_player'] = player1_name

            game_html = GAME_HTML.format(player1_name=player1_name, player2_name=player2_name, game_name=game_name)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(game_html.encode('utf-8'))
            
        elif self.path == "/handle_mouse_position":
            
            game = self.session_data.get('game')
            table = self.session_data.get('table')
            game_name = self.session_data.get('game_name')
            player1_name = self.session_data.get('player1_name')
            player2_name = self.session_data.get('player2_name')
            current_player = self.session_data.get('current_player', player1_name)

            if game is None or table is None or self.session_data.get('game_over'):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No active game')
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            vx = data['vx']
            vy = data['vy']

            game.shoot(game_name, current_player, table, vx, vy)

            final_table = game._final_table
            svgs = list(game._shot_svgs)

            next_player = player2_name if current_player == player1_name else player1_name
            response = {"svgs": svgs, "current_player": next_player}

            eight_ball_on_table = has_ball(final_table, 8)

            if not eight_ball_on_table:
                response["winner"] = next_player
                self.session_data['game_over'] = True
            else:
                cue_ball = final_table.cueBall(final_table)
                if cue_ball is None:
                    pos = Physics.Coordinate(675, 2025)
                    sb = Physics.StillBall(0, pos)
                    final_table += sb
                    svgs.append(final_table.svg())

                self.session_data['table'] = final_table
                self.session_data['current_player'] = next_player

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            # generate 404 for POST requests that aren't handled above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))




def has_ball(table, number):
    for obj in table:
        if obj is not None:
            if isinstance(obj, Physics.StillBall) and obj.obj.still_ball.number == number:
                return True
            if isinstance(obj, Physics.RollingBall) and obj.obj.rolling_ball.number == number:
                return True
    return False

def nudge():
    return random.uniform( -1.5, 1.5 );

def createNewTable():
    table = Physics.Table()

    # Define the positions of the balls from the SVG
    ball_positions = [
        (675, 2025),  # Cue ball
        (675, 675),   # Apex ball
        (615, 630),   # Second row
        (735, 630),
        (555, 585),   # Third row
        (675, 585),
        (795, 585),
        (495, 540),   # Fourth row
        (615, 540),
        (735, 540),
        (855, 540)
        # Add more rows as needed
    ]

    for ball_id, (x, y) in enumerate(ball_positions, start=0):
        pos = Physics.Coordinate(x, y)
        sb = Physics.StillBall(ball_id, pos)
        table += sb

    return table


def createNewTableAndSave():
    # Generate the table
    table = createNewTable()


if __name__ == "__main__":
    createNewTableAndSave()
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
