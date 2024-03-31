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

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/index.html' ]:

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
        # hanle post request
        # parse the URL to get the path and form data
        if self.path == "/handle_mouse_position":

            db = Physics.Database()

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            vx = data['vx']
            vy = data['vy']

            # Now you can use finalX and finalY for your purpose
            print("Received vx:", vx)
            print("Received vy:", vy)

            table = createNewTable()

            game = Physics.Game( gameName="Game 01", player1Name="Stefan", player2Name="Efren Reyes" );
            game.shoot( "Game 01", "Stefan", table, vx, vy);


            tableID = 0
            
            svgs = []
            table = db.readTable(tableID)

            svgs.append(HEADER);
            print(svgs);

            while table is not None:
                svgdata = table.svg()
                svgs.append(svgdata)     
                tableID += 1
                table = db.readTable(tableID)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_json = json.dumps(svgs)
            self.wfile.write(response_json.encode('utf-8'))
            # self.wfile.write(bytes("Data received successfully!", "utf-8"))


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























# import sys;
# import os; 
# import cgi;
# import Physics;
# import math;

# from http.server import HTTPServer;
# from http.server import BaseHTTPRequestHandler;

# from urllib.parse import urlparse, parse_qsl;

# HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
# "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
# xmlns="http://www.w3.org/2000/svg"
# xmlns:xlink="http://www.w3.org/1999/xlink">
# <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0";"/>""";


# class MyHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # parse the URL to get the path and form data
#         parsed  = urlparse( self.path );

#         # check if the web-pages matches the list
#         if parsed.path in [ '/startPage.html' ]:

#             # retreive the HTML file
#             fp = open( '.'+self.path );
#             content = fp.read();

#             # generate the headers
#             self.send_response( 200 ); # OK
#             self.send_header( "Content-type", "text/html" );
#             self.send_header( "Content-length", len( content ) );
#             self.end_headers();

#             # send it to the broswer
#             self.wfile.write( bytes( content, "utf-8" ) );
#             fp.close();

#         #ensures that it is a valid svg file before trying to read it
#         elif parsed.path.endswith('.svg'):
            
#             fp = open( '.'+self.path, 'rb' );
#             content = fp.read();
#             self.send_response(200);
#             self.send_header('Content-type', 'image/svg+xml');
#             self.send_header('Content-length', len(content));
#             self.end_headers();
#             self.wfile.write(content);
#             fp.close();

#         elif parsed.path == '/script.js':
#             with open('script.js', 'rb') as fp:
#                 content = fp.read()

#             # Send a 200 OK response with the JavaScript content
#             self.send_response(200)
#             self.send_header('Content-type', 'application/javascript')
#             self.send_header('Content-length', len(content))
#             self.end_headers()
#             self.wfile.write(content)

#         elif parsed.path == '/styles.css':
#             with open('styles.css', 'rb') as fp:
#                 content = fp.read()

#             # Send a 200 OK response with the JavaScript content
#             self.send_response(200)
#             self.send_header('Content-type', 'text/css')
#             self.send_header('Content-length', len(content))
#             self.end_headers()
#             self.wfile.write(content)


#         else:
#             # generate 404 for GET requests that aren't the 3 files above
#             self.send_response( 404 );
#             self.end_headers();
#             self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

#     def do_POST(self):
#         # hanle post request
#         # parse the URL to get the path and form data
#         parsed  = urlparse( self.path );

#         if parsed.path in [ '/startPageInfo.html' ]:

#             # get data send as Multipart FormData (MIME format)
#             form = cgi.FieldStorage( fp=self.rfile,
#                                      headers=self.headers,
#                                      environ = { 'REQUEST_METHOD': 'POST',
#                                                  'CONTENT_TYPE': 
#                                                    self.headers['Content-Type'],
#                                                } 
#                                    );
                                
                                

#             # Delete all svg files
#             for filename in os.listdir('.'):
#                 if filename.startswith('table-') and filename.endswith('.svg'):
#                     os.remove(filename)

#             # Access form data for Still Ball
#             #casted as unsigned char & doubles(floats)
#             if 'player1_name' not in form or 'player2_name' not in form or 'game_name' not in form:
#                 # Handle the case where one or more form fields are missing
#                 # You can return an error response or redirect the user to the form page with an error message
#                 # For example:
#                 self.send_response(400)  # Bad Request
#                 self.end_headers()
#                 self.wfile.write(b"Missing form fields")
#                 return

#             # Access form data for player names and game name
#             player1NameForm = form['player1_name'].value.strip()
#             player2NameForm = form['player2_name'].value.strip()
#             gameNameForm = form['game_name'].value.strip()

#             # Check if any of the form fields are empty after stripping whitespace
#             if not player1NameForm or not player2NameForm or not gameNameForm:
#                 # Handle the case where one or more form fields are empty
#                 # You can return an error response or redirect the user to the form page with an error message
#                 # For example:
#                 self.send_response(400)  # Bad Request
#                 self.end_headers()
#                 self.wfile.write(b"One or more form fields are empty")
#                 return

#             # create a table and objects to that table
#             table = Physics.Table();
#             Physics.Table.setUpTable(table);
#             game = Physics.Game(gameName = gameNameForm, player1Name = player1NameForm, player2Name = player2NameForm);
        
#             f = open("StartTable.svg","w");
#             f.write(table.svg());

#             svgList = []
#             svgList.append(Physics.HEADER);

#             for i in table:
#                 if i is not None:
#                     if i.obj.still_ball.number == 0 and isinstance(i, Physics.StillBall):
#                         cueBallString = """ <circle id="cueBall" cx="{}" cy="{}" r="28.5" fill="WHITE" onclick="trackon();"/>\n """.format(i.obj.still_ball.pos.x, i.obj.still_ball.pos.y);
#                         svgList.append(cueBallString);
#                         continue;
#                     svgList.append(i.svg());

#             cueX1 = table[10].obj.still_ball.pos.x;
#             cueY1 = table[10].obj.still_ball.pos.y;

#             # cueX2 = cueX1 + cueStickLength * math.cos(math.radians(angle));
#             cueX2 = cueX1 + 100;
#             cueY2 = cueY1 + 100;

#             # Generate HTML for display
#             response_html = """
#             <html>
#             <head>
#                 <title>Form Response</title>
#                 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
#                 <script src="script.js"></script>
#                 <link rel="stylesheet" type="text/css" href="styles.css">
#             </head>
#             <body>
#                 <h2>Form Response</h2>
#                 <a href="startPage.html">Back</a>
#                 <p>Player1Name: {player1Name}</p>
#                 <p>Player2Name: {player2Name}</p>
#                 <p>Game Name: {gameName}</p>
#                 <div id="svgDiv">
#                 <svg version="1.1" width="700" height="1375" viewBox="-25 -25 1400 2750" xmlns="http://www.w3.org/2000/svg" onmousemove="trackit(event)">""".format(player1Name=player1NameForm, player2Name=player2NameForm, gameName=gameNameForm)
#             for i in svgList:
#                 response_html += i;
#             response_html += """ 
#                     <line id="cueStick" x1="{}" y1="{}" x2="{}" y2="{}" style="stroke: black; stroke-width: 10;"  />
#                     </svg>
#                 </div>
#             </body>
#             </html>""".format(cueX1, cueY1, cueX2, cueY2);
#             # Send response to the browser
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(response_html.encode('utf-8'))




#         else:
#             # generate 404 for POST requests that aren't the file above
#             self.send_response( 404 );
#             self.end_headers();
#             self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );
        



# if __name__ == "__main__":
#     httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
#     print( "Server listing in port:  ", int(sys.argv[1]) );
#     httpd.serve_forever();
