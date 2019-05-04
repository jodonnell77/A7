"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# John O'Donnel (jro79) and Anthony Nguyen (an523)
# 4/27/2019
"""
from game2d import *
from consts import *
from models import *

import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_aliens(self):
        "Getter for _aliens attibute in Wave"
        return self._aliens

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        self._ship = Ship(400,SHIP_BOTTOM,'ship.png')
        self.create_aliens()

#        assert is_instance(ship, Ship)
#        if(type(aliens) != list):
#            assert aliens == None
#        for i in range(len(aliens)):
#            for ii in range(len(aliens[i])):
#                assert is_instance(aliens[i][ii],Alien)
#        assert is_instance(bolts, list)
#        for i in bolts:
#            assert is_instance(i,Bolt)
#        assert is_instance(dline,GPath)
#        assert is_instance(lives, int) and lives >= 0
#        assert time >= 0
    def create_aliens(self):
        """
        Creates the list of aliens in their respective positions.
        """
        self._aliens =[]
        upper = GAME_HEIGHT-ALIEN_CEILING
        x=ALIEN_H_SEP + ALIEN_WIDTH*.5
        base = upper-(ALIEN_HEIGHT+ALIEN_V_SEP)*ALIEN_ROWS
        n=0 #image looper
        for up in range(ALIEN_ROWS):
            group = []
            source = ALIEN_IMAGES[int(n)]
            n+=0.5 ## maketwo same imagers per rows
            if n == 3: #resets image loop
                n=0
            for across in range(ALIENS_IN_ROW):

                group.append(Alien(x+(ALIEN_WIDTH+ALIEN_H_SEP)*(across)\
                ,base + (ALIEN_HEIGHT+ALIEN_V_SEP)*(up),source))
            self._aliens.append(group)
        return self._aliens





    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input):
        assert isinstance(input,GInput)

        if input.is_key_down('left'):
            self._ship.move_ship('left')
        elif input.is_key_down('right'):
            self._ship.move_ship('right')

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """Calls the draw function for Ship, Aliens, Defensive Line, and Bolts"""
        self.draw_wave_aliens(view)
        self._ship.draw(view)

    def draw_wave_aliens(self,view):
        """
        Draw the wave of aliens
        """
        for row in range(len(self.get_aliens())):
            for column in range(len(self.get_aliens()[row])):
                alien=self.get_aliens()[row][column]
                if (alien != None):
                    alien.draw(view) #drawing gimage


    # HELPER METHODS FOR COLLISION DETECTION
