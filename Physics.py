import phylib;
import Physics;
import math;
import random;

import os;
import sqlite3;


HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" onmousemove="trackit(event)" />""";

FOOTER = """</svg>\n""";

def write_svg(table_id, table):
    with open("table%4.2f.svg" % table.time, "w") as fp:
        fp.write(table.svg())

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL    = 0.01

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_STILL_BALL, number, pos, None, None, 0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        colour_index = self.obj.still_ball.number % len(BALL_COLOURS)
        # return """ <circle cx="%d" cy="%d" r="%d" fill="%d" />\n"""%(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)])
        return """ <circle cx="{}" cy="{}" r="{}" fill="{}" />\n""".format(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[colour_index])


class RollingBall(phylib.phylib_object):
    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0)
        self.__class__ = RollingBall
    
    def svg(self):
        colour_index = self.obj.rolling_ball.number % len(BALL_COLOURS)
        # return """ <circle cx="%d" cy="%d" r="%d" fill="%d" />\n"""%(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)])
        return """ <circle cx="{}" cy="{}" r="{}" fill="{}" />\n""".format(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[colour_index])



class Hole(phylib.phylib_object):
    def __init__(self,pos):
        phylib.phylib_object.__init(self, phylib.PHYLIB_HOLE, pos);
        self.__class__ = Hole;

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n"""%(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);



class HCushion(phylib.phylib_object):
    def __init__(self, y):
        phylib.phylib_object.__init(self, phylib.PHYLIB_HCUSHION, y);
        self.__class__ = HCushion;


    def svg(self):
        if self.obj.hcushion.y == 0:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n"""%(self.obj.hcushion.y -25);
        elif self.obj.hcushion.y == 2700:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n"""%(self.obj.hcushion.y);



class VCushion(phylib.phylib_object):
    def __init__(self, x):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_VCUSHION, x);
        self.__class__ = VCushion;

    def svg(self):
        if self.obj.vcushion.x == 0:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n"""%(self.obj.vcushion.x - 25);
        elif self.obj.vcushion.x == 1350:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n"""%(self.obj.vcushion.x)

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        self.current = -1;
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    #Added my own method in order to add a ball to the table at a given index
    def __setitem__(self, index, value):
        if index >= 0 and index < MAX_OBJECTS:
            self.add_object_index(value,index)
        else:
            raise IndexError("Index out of range")

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        newString = HEADER;
        for obj in self:
            if obj is not None:
                newString += obj.svg();
        newString += FOOTER;
        return newString;

    def setUpTable(self):
        # cue 
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 + 2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0)
        sb = Physics.StillBall(0, pos)
        self += sb
        
        ### FIRST ROW ###
        # 1 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_WIDTH / 2.0)
        sb = Physics.StillBall(1, pos)
        self += sb

        ### SECOND ROW ###
        # 2 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER + 4.0) / 2.0, Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0))
        sb = Physics.StillBall(2, pos)
        self += sb
        # 3 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 4.0) / 2.0,
                                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0))
        sb = Physics.StillBall(3, pos)
        self += sb

        ### THIRD ROW ###
        # 4 ball
        pos = Physics.Coordinate((Physics.TABLE_WIDTH / 2.0) - (4 + Physics.BALL_DIAMETER) + nudge(), (Physics.TABLE_WIDTH / 2.0) - 107.0)
        sb = Physics.StillBall(4, pos)
        self += sb

        # 5 ball
        pos = Physics.Coordinate((Physics.TABLE_WIDTH / 2.0) + (4 + Physics.BALL_DIAMETER) + nudge(), (Physics.TABLE_WIDTH / 2.0) - 107.0)
        sb = Physics.StillBall(5, pos)
        self += sb

        # 8 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, (Physics.TABLE_WIDTH / 2.0) - 107.0)
        sb = Physics.StillBall(8, pos)
        self += sb

        ### FOURTH ROW ###
        # 6 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER + 4.0) / 2.0, Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) - 107.0)
        sb = Physics.StillBall(6, pos)
        self += sb
        # 7 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 4.0) / 2.0, Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) - 107.0)
        sb = Physics.StillBall(7, pos)
        self += sb
        # 9 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 + (( 3.18 * Physics.BALL_DIAMETER) + 4.0) / 2.0, Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) - 107.0)
        sb = Physics.StillBall(9, pos)
        self += sb

        # 10 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 - (( 3.18 * Physics.BALL_DIAMETER) + 4.0) / 2.0, Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) - 107.0)
        sb = Physics.StillBall(10, pos)
        self += sb

        ### FIFTH ROW ###
        # 11 ball
        pos = Physics.Coordinate((Physics.TABLE_WIDTH / 2.0) - (4 + Physics.BALL_DIAMETER) + nudge(), (Physics.TABLE_WIDTH / 2.0) - (2 * 107.0))
        sb = Physics.StillBall(11, pos)
        self += sb
        # 12 ball
        pos = Physics.Coordinate((Physics.TABLE_WIDTH / 2.0) + (4 + Physics.BALL_DIAMETER) + nudge(), (Physics.TABLE_WIDTH / 2.0) - (2 * 107.0))
        sb = Physics.StillBall(12, pos)
        self += sb
        # 13 ball
        pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, (Physics.TABLE_WIDTH / 2.0) - (2 * 107.0))
        sb = Physics.StillBall(13, pos)
        self += sb

        # 14 ball
        pos = Physics.Coordinate((Physics.TABLE_WIDTH / 2.0) + (4 + (2.08 * Physics.BALL_DIAMETER)) + nudge(), (Physics.TABLE_WIDTH / 2.0) - (2 * 107.0))
        sb = Physics.StillBall(14, pos)
        self += sb

        # 15 ball
        pos = Physics.Coordinate((Physics.TABLE_WIDTH / 2.0) - (4 + (2.08 * Physics.BALL_DIAMETER)) + nudge(), (Physics.TABLE_WIDTH / 2.0) - (2 * 107.0))
        sb = Physics.StillBall(15, pos)
        self += sb


    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,Coordinate(0,0),Coordinate(0,0),Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
        
                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,Coordinate( ball.obj.still_ball.pos.x,ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall(self, table):
        for objects in table:
            if (isinstance (objects, StillBall) or isinstance(objects, RollingBall)):
                if objects.obj.rolling_ball.number == 0:
                    return objects;
                elif objects.obj.still_ball.number == 0:
                    return objects;

    
class Database():

    def __init__(self, reset = False):
        self.db = 'phylib.db';
        if reset == True:
            if os.path.exists(self.db ):
                os.remove(self.db );
        
        self.conn = sqlite3.connect(self.db);
        self.cur = self.conn.cursor();

    ### CREATE TABLES ###
    def createDB(self):

        self.cur = self.conn.cursor();

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Ball(
                    BALLID  INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                    BALLNO  INTEGER  NOT NULL,
                    XPOS    FLOAT    NOT NULL,
                    YPOS    FLOAT    NOT NULL,
                    XVEL    FLOAT,
                    YVEL    FLOAT 
        )""");


        self.cur.execute("""CREATE TABLE IF NOT EXISTS TTable(
                    TABLEID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    TIME    FLOAT   NOT NULL
        ) """);

        self.cur.execute("""CREATE TABLE IF NOT EXISTS BallTable(
                    BALLID      INTEGER NOT NULL,
                    TABLEID     INTEGER NOT NULL,
                    FOREIGN KEY (BALLID) REFERENCES Ball,
                    FOREIGN KEY (TABLEID) REFERENCES TTable
        ) """);

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Shot(
                    SHOTID      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    PLAYERID    INTEGER NOT NULL,
                    GAMEID      INTEGER NOT NULL,
                    FOREIGN KEY (PLAYERID) REFERENCES Player,
                    FOREIGN KEY (GAMEID) REFERENCES Game
        )""");

        self.cur.execute("""CREATE TABLE IF NOT EXISTS TableShot(
                    TABLEID     INTEGER NOT NULL,
                    SHOTID      INTEGER NOT NULL,
                    FOREIGN KEY (TABLEID) REFERENCES TTable,
                    FOREIGN KEY (SHOTID) REFERENCES Shot
        ) """);

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Game(
                    GAMEID    INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
                    GAMENAME  VARCHAR(64)  NOT NULL
        ) """);

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Player(
                    PLAYERID     INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
                    GAMEID       INTEGER      NOT NULL,
                    PLAYERNAME   VARCHAR(64)  NOT NULL,
                    FOREIGN KEY  (GAMEID)  REFERENCES Game
        ) """);

        self.cur.close();
        self.conn.commit();


    def readTable(self, tableID):

        self.cur = self.conn.cursor();
        self.cur.execute("""SELECT COUNT(*) FROM BallTable WHERE TABLEID = ?""", (tableID + 1,));
        count = self.cur.fetchone()[0];

        if count == 0:
            #the tableID was not found
            return None;

        returnTable = Physics.Table();
    

        self.cur.execute("""SELECT TIME FROM TTable WHERE TABLEID = ?""",(tableID + 1,));
        returnTable.time = self.cur.fetchone()[0];

        #Getting the balls with maxIDs
        self.cur.execute("""SELECT Ball.BALLNO, MAX(Ball.BALLID) 
                            FROM BallTable 
                            JOIN Ball ON BallTable.BALLID = Ball.BALLID 
                            WHERE BallTable.TABLEID = ? 
                            GROUP BY Ball.BALLNO""", (tableID + 1,));
        max_ballIDs = dict(self.cur.fetchall());

        self.cur.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL 
                            FROM BallTable
                            JOIN Ball ON BallTable.BALLID = Ball.BALLID
                            WHERE BallTable.TABLEID = ?""", (tableID + 1,));

        ball_list = self.cur.fetchall();

        for ball in ball_list:
            ball_num = ball[1];
            ball_pos = Physics.Coordinate(ball[2], ball[3]);

            if ball[0] == max_ballIDs.get(ball_num):
                #The ball is a still ball
                if ball[4] == 0 and ball[5] == 0:
                    new_sb = Physics.StillBall(ball_num,ball_pos);
                    # if ball[0] == max_ballIDs[ball_num][1]:
                    returnTable += new_sb;
                    
                else:
                    ball_vel = Physics.Coordinate(float(ball[4]),float(ball[5]));
                    ball_acc_x = 0.0;
                    ball_acc_y = 0.0;

                    ball_speed = phylib.phylib_length(ball_vel);

                    if ball_speed > VEL_EPSILON:
                        ball_acc_x = (-ball[4] / ball_speed) * DRAG;
                        ball_acc_y = (-ball[5] / ball_speed) * DRAG;
                    
                    ball_acc = Physics.Coordinate(ball_acc_x,ball_acc_y);

                    new_rb = Physics.RollingBall(ball_num,ball_pos,ball_vel,ball_acc);
                    # if ball[0] == max_ballIDs[ball_num][1]:
                    returnTable += new_rb;

        self.cur.close();
        self.conn.commit();
        return returnTable;

    def writeTable(self, table):
        self.cur = self.conn.cursor()

        self.cur.execute("""INSERT INTO TTable (TIME)
                            VALUES (?) """, (table.time,))

        tableID = self.cur.lastrowid - 1

        for obj in table:
            if isinstance(obj, StillBall):
                ball_num = obj.obj.still_ball.number
                pos_x = obj.obj.still_ball.pos.x
                pos_y = obj.obj.still_ball.pos.y
                vel_x = 0.0
                vel_y = 0.0
            elif isinstance(obj, RollingBall):
                ball_num = obj.obj.rolling_ball.number
                pos_x = obj.obj.rolling_ball.pos.x
                pos_y = obj.obj.rolling_ball.pos.y
                vel_x = obj.obj.rolling_ball.vel.x
                vel_y = obj.obj.rolling_ball.vel.y
            else:
                continue

            self.cur.execute("""INSERT OR IGNORE INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                VALUES (?,?,?,?,?)""", (ball_num, pos_x, pos_y, vel_x, vel_y))
            
            ballID = self.cur.lastrowid

            self.cur.execute("""INSERT INTO BallTable (BALLID, TABLEID) 
                                VALUES (?, ?)""", (ballID, tableID + 1))
            
        self.cur.close()
        self.conn.commit()

        return tableID + 1;

    def close(self):
        self.conn.commit();
        self.conn.close();

    #! NEED TO CHECK THIS
    def getGame(self, GameID):
        self.cur = self.conn.cursor();

        self.cur.execute("""SELECT COUNT(*) FROM BallTable WHERE TABLEID = ?""", (GameID + 1,));
        count = self.cur.fetchone()[0];

        if count == 0:
            #the tableID was not found
            print("Game with ID:", GameID, "not found.");
            return None;

        self.cur.execute("""SELECT G.GAMENAME, P1.PLAYERNAME AS PLAYER1NAME, P2.PLAYERNAME AS PLAYER2NAME
                            FROM Game G
                            JOIN Player P1 ON G.GAMEID = P1.GAMEID AND P1.PLAYERID = (SELECT MIN(PLAYERID) FROM Player WHERE GAMEID = G.GAMEID)
                            JOIN Player P2 ON G.GAMEID = P2.GAMEID AND P2.PLAYERID = (SELECT MAX(PLAYERID) FROM Player WHERE GAMEID = G.GAMEID)
                            WHERE G.GAMEID = ?""", (GameID + 1,));
        row = self.cur.fetchone();
        
        self.cur.close();
        self.conn.commit();

        if row:
            return row;
        else:
            return None;

    def setGame(self,gameName, player1Name, player2Name):
        self.cur = self.conn.cursor();

        self.cur.execute("""INSERT INTO Game (GAMENAME) 
                       VALUES (?)""",(gameName,));

        self.cur.execute("""SELECT GAMEID FROM Game 
                            WHERE GAMENAME = ?""",(gameName,));
        gameID = self.cur.fetchone()[0];
        
        self.cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) 
                       VALUES (?,?)""",(gameID, player1Name));

        self.cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) 
                       VALUES (?,?)""",(gameID, player2Name));

        self.cur.close();
        self.conn.commit();
        return_list = [gameID,gameName,player1Name,player2Name];
        return return_list;
        # return gameID;


    def newShot(self,playerName):
        self.cur = self.conn.cursor();

        #gets the playerID & GameID based on the player name
        self.cur.execute("""SELECT PLAYERID, GAMEID FROM Player WHERE PLAYERNAME = ?""",(playerName,));
        
        id_list = self.cur.fetchone() 
        playerID = id_list[0]
        gameID = id_list[1]

        self.cur.execute("""INSERT INTO Shot (PLAYERID, GAMEID) 
                       VALUES (?,?)""",(playerID,gameID));

        self.cur.execute("""SELECT SHOTID FROM Shot
                       WHERE PLAYERID = ? AND GAMEID = ?""",(playerID,gameID));

        shotID = self.cur.fetchone()[0];

        self.cur.close();
        self.conn.commit();

        #returns the SHOTID
        return shotID;

    def saveTableShot(self,tableID, shotID):
        self.cur = self.conn.cursor();
        self.cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
                            VALUES (?,?)""",(tableID,shotID));

        self.cur.close();
        self.conn.commit();
        



class Game():

    def __init__(self, gameID = None, gameName = None, player1Name = None, player2Name = None):
        # self.new_db = Database( reset=True );
        self.new_db = Database();
        self.new_db.createDB();

        if gameID is not None and (gameName is None and player1Name is None and player2Name is None):
            self.gameID = gameID + 1;

            # gets a list that contains the game and players' names
            game_list = self.new_db.getGame(gameID);
            if game_list is not None:
                self.gameName = game_list[0];
                self.player1Name = game_list[1];
                self.player2Name = game_list[2];
            

        elif gameID is None and (gameName is not None and player1Name is not None and player2Name is not None):
            game_list = self.new_db.setGame(gameName,player1Name,player2Name);

            # gets a list that contains the game and players' names as well as the gameID
            self.gameID = game_list[0];
            self.gameName = game_list[1];
            self.player1Name = game_list[2];
            self.player2Name = game_list[3];
        
        else: 
            raise TypeError("Invalid combination of arguments provided to the constructor")

    def shoot(self, gameName, playerName, table, xvel, yvel):
        shotID = self.new_db.newShot(playerName);
        new_cue_ball = table.cueBall(table);

        pos_x = new_cue_ball.obj.rolling_ball.pos.x;
        pos_y = new_cue_ball.obj.rolling_ball.pos.y;

        new_cue_ball.type = phylib.PHYLIB_ROLLING_BALL;
        new_cue_ball.obj.rolling_ball.number = 0;

        new_cue_ball.obj.rolling_ball.pos.x = pos_x;
        new_cue_ball.obj.rolling_ball.pos.y = pos_y;

        new_cue_ball.obj.rolling_ball.vel.x = xvel;
        new_cue_ball.obj.rolling_ball.vel.y = yvel;

        new_cue_ball.vel = Physics.Coordinate(xvel,yvel);
        speed = phylib.phylib_length(new_cue_ball.vel);

        acc_x = 0.0;
        acc_y = 0.0;

        if (speed > VEL_EPSILON):
            acc_x = (- xvel / speed) * DRAG;
            acc_y = (- yvel / speed) * DRAG;

        new_cue_ball.obj.rolling_ball.acc.x = acc_x;
        new_cue_ball.obj.rolling_ball.acc.y = acc_y;

        new_cue_ball.acc = Coordinate(acc_x,acc_y);
        
        while table is not None:
            start_time = table.time;
            new_table = table;
            table = table.segment();

            if table is not None:
                end_time = table.time;

            elapsed_time = end_time - start_time;
            frames = int(elapsed_time / FRAME_INTERVAL);

            for frame in range(frames):
                new_time = frame * FRAME_INTERVAL;
                copyTable = new_table.roll(new_time);
                copyTable.time = start_time + new_time;

                tableID = self.new_db.writeTable(copyTable);
                write_svg(tableID, copyTable);
                self.new_db.saveTableShot(tableID, shotID);

        return shotID;

def nudge():
    return random.uniform( -1.5, 1.5 );