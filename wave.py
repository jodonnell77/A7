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
        _exists_player_bolt: boolean if a Ship Bolt is in the _bolts list
        _direction: the direction the aliens are currently moving
                    (string "left" or "right")
        _steps_until_fire: the number of steps until the aliens fire (int >= 0)
        _steps: the number of steps since last alien fired (int >= 0)
        _dead_count: number of aliens eliminated (int >= 0)
        _dline_breached: True or False if aliens have breached the dline
        _ship_alive: True or False if the ship is currenty alive
        _missed_shots: number of missed shots (int >= 0)
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_aliens(self):
        """
        Getter for _aliens attibute in Wave
        """
        return self._aliens
    def get_missed_shots(self):
        """
        Getter for _missed_shots in Wave
        """
        return self._missed_shots
    def get_ship_alive(self):
        """
        Getter for _ship_alive attibute in Wave
        """
        return self._ship_alive

    def set_ship_alive(self):
        """
        Setter for _ship_alive attibute in Wave
        """
        self._ship_alive = True

    def get_dline_breached(self):
        """
        Getter for _dline_brached attibute in Wave
        """
        return self._dline_breached

    def get_dead_count(self):
        """
        Getter for _dead_count attibute in Wave
        """
        return self._dead_count
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Ititializer for the Wave class
        """
        self._ship = Ship(400,SHIP_BOTTOM,'ship.png')
        self.create_aliens()
        self.create_dline()
        self._time = 0
        self._bolts = []
        self._exists_player_bolt = False
        self._direction = 'right'
        self._steps = 0
        self._steps_until_fire = None
        self._ship_alive = True
        self._dline_breached = False
        self._dead_count = 0
        self._missed_shots = 0
        self._left_barrier = Barrier(LEFT_BARRIER_X,LEFT_BARRIER_Y,BARRIER_HEIGHT,BARRIER_WIDTH,10)
        self._right_barrier = Barrier(RIGHT_BARRIER_X,RIGHT_BARRIER_Y,BARRIER_HEIGHT,BARRIER_WIDTH,10)


    def create_aliens(self):
        """
        Creates the list of aliens in their respective positions, drawing from
        left to right, upwards. Images of every two rows of aliens cycles through
        ALIEN_IMAGES[n] where n goes from 0 to 2.
        """
        self._aliens =[]
        upper = GAME_HEIGHT-ALIEN_CEILING
        x=ALIEN_H_SEP + ALIEN_WIDTH*.5
        base = upper-(ALIEN_HEIGHT+ALIEN_V_SEP)*ALIEN_ROWS
         #image looper
        for across in range(ALIENS_IN_ROW):
            group = []
            n=0
            for up in range(ALIEN_ROWS):
                source = ALIEN_IMAGES[int(n)]
                n+=0.5 ## maketwo same imagers per rows
                if n == 3: #resets image loop
                    n=0
                group.append(Alien(x+(ALIEN_WIDTH+ALIEN_H_SEP)*(across)\
                ,base + (ALIEN_HEIGHT+ALIEN_V_SEP)*(up),source))
            self._aliens.append(group)
        return self._aliens

    def create_dline(self):
        """
        Creates the defensive line with x position spanning from 0 to the GAME_WIDTH,
        and y position DEFENSE_LINE above 0
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
        linewidth=2, linecolor = "white")
        return self._dline
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input, dt):
        """
        Calls update method for Ship, Aliens, Laser Bolts, and Dline

        Parameter: input is a user input
        Precondition: input is a valid GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time+=dt
        self.update_ship(input)
        self.move_aliens(dt)
        self.update_bolts(input)
        self.ship_collisions()
        self.alien_collisions()
        self.alien_dline_collision()
        self.barrier_collision()

    def update_ship(self,input):
        """
        Takes user input to update the position of the ship

        Parameter: input is a user input
        Precondition: input is a valid GInput
        """
        assert isinstance(input,GInput)
        if input.is_key_down('left'):
            self._ship.move_ship('left')
        elif input.is_key_down('right'):
            self._ship.move_ship('right')

    def update_bolts(self, input):
        """
        Handles updates for player bolts and alien bolts

        Parameter: input is a user input
        Precondition: input is a valid GInput
        """
        self.player_bolts(input)
        self.alien_bolts()

    def player_bolts(self, input):
        """
        Creates and moves the player bolts; Removes it once it leaves the game window

        Parameter: input is a user input
        Precondition: input is a valid GInput
        """
        if input.is_key_down('spacebar') and self._exists_player_bolt == False:
            print('pew')
            self._bolts.append(Bolt(self._ship.get_ship_x(),SHIP_BOTTOM + SHIP_HEIGHT,\
             BOLT_SPEED, 'player'))
            self._exists_player_bolt = True

        for bolt in self._bolts:
            if bolt._kind == "player":
                bolt.move_bolt_up()
            if bolt.get_kind_bolt() == 'player' and bolt.get_bolt_y() >= GAME_HEIGHT:
                self._bolts.remove(bolt)
                self._missed_shots += 1
                self._exists_player_bolt = False
                print("pew gone")

    def move_aliens(self, dt):
        """
        Determines whether to move aliens to the left or to the right. When the
        aliens hit the right wall it changes their direction to left and vice versa.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        down = False
        right_end = GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH/2
        left_end = 0 + ALIEN_H_SEP + ALIEN_WIDTH/2
        if self._direction == "right":
            self.move_aliens_right()
        if self._direction == "left":
            self.move_aliens_left()

        for row in range(len(self.get_aliens())):
            for column in range(len(self.get_aliens()[row])):
                alien=self.get_aliens()[row][column]
                if (alien != None):
                    if alien.x > right_end:
                        self._direction = "left"
                        down = True
                    if alien.x < left_end:
                        self._direction = "right"
                        down = True

        if down == True and self._time < dt:
            self.move_aliens_down()
            down = False

    def move_aliens_right(self):
        """
        Moves the aliens to the right until they hit the wall.
        For every alien eliminated, all other aliens move SPEED_UP time
        faster between steps
        """
        right_end = GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH/2
        if self._time >= ALIEN_SPEED*(SPEED_UP**self.get_dead_count()):
            self._time = 0
            self._steps += 1
            for row in range(len(self.get_aliens())):
                for column in range(len(self.get_aliens()[row])):
                    alien=self.get_aliens()[row][column]
                    if (alien != None):
                        alien.x += ALIEN_H_WALK

    def move_aliens_left(self):
        """
        Moves the aliens to the left until they hit the wall.
        For every alien eliminated, all other aliens move SPEED_UP time
        faster between steps
        """

        left_end = 0 + ALIEN_H_SEP + ALIEN_WIDTH/2
        if self._time >= ALIEN_SPEED*(SPEED_UP**self.get_dead_count()):
            self._time = 0
            self._steps += 1
            for row in range(len(self.get_aliens())):
                for column in range(len(self.get_aliens()[row])):
                    alien=self.get_aliens()[row][column]
                    if (alien != None):
                        alien.x -= ALIEN_H_WALK

    def move_aliens_down(self):
        """
        Method which moves the aliens downward
        """
        for row in range(len(self.get_aliens())):
            for column in range(len(self.get_aliens()[row])):
                alien=self.get_aliens()[row][column]
                if (alien != None):
                    alien.y -= ALIEN_V_WALK
                    if self._direction == "right":
                        alien.x += ALIEN_H_WALK
                    if self._direction == "left":
                        alien.x -= ALIEN_H_WALK

    def alien_bolts(self):
        """
        Creates and moves the alien bolts; removes it once it leaves the game window.
        If the alien has just fired 0 steps ago, _steps_until_fire will be assigned
        a random integer value within 0 to BOLT_RATE. Once the alien has moved that
        many _steps, a bolt will be formed. The bolt is formed by choosing a random
        column of aliens and finding the minimum of all the values of the alien's
        y position within that column.
        """


        if self._steps== 0:
            self._steps_until_fire = random.randint(1,BOLT_RATE)
        if self._steps == self._steps_until_fire:
            aliens = self.get_aliens()
            y = []
            #finds a random column of aliens
            column = random.randint(0, len(aliens) - 1 )
            while aliens[column].count(None) == ALIEN_ROWS:
                column = random.randint(0, len(aliens) - 1 )

            for i in aliens[column]:
                if(i != None):
                    y.append(i.y)
                    x=i.x
            #creates a bolt at the coordinate of the sait alien
            self._bolts.append(Bolt(x,min(y), BOLT_SPEED, "alien", "purple" ))
            self._steps = 0 #bolt has just fired 0 steps ago
        for bolt in self._bolts:
            if bolt._kind == "alien":
                bolt.move_bolt_down()
                if bolt.x > self._ship.get_ship_x():
                    bolt.move_bolt_side(random.randint(-HEAT_SEEKING_DIFFICULTY,0))
                if bolt.x < self._ship.get_ship_x():
                    bolt.move_bolt_side(random.randint(0,HEAT_SEEKING_DIFFICULTY))
            if bolt.get_kind_bolt() == 'alien' and bolt.get_bolt_y() < 0:
                self._bolts.remove(bolt)
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Calls the draw functions for Ship, Aliens, Defensive Line, and Bolts
        """
        self.draw_wave_aliens(view)
        self.draw_ship(view)
        self.draw_dline(view)
        self.draw_bolt(view)
        self.draw_barriers(view)

    def draw_wave_aliens(self,view):
        """
        Draw the wave of aliens
        """
        for row in range(len(self.get_aliens())):
            for column in range(len(self.get_aliens()[row])):
                alien=self.get_aliens()[row][column]
                if (alien != None):
                    alien.draw(view) #drawing gimage

    def draw_ship(self,view):
        """
        Draw the ship
        """
        self._ship.draw(view)

    def draw_dline(self,view):
        """
        Draws the defensive line
        """
        self._dline.draw(view)

    def draw_bolt(self,view):
        """
        Draws the Bolts
        """

        for i in self._bolts:
            i.draw(view)
    def draw_barriers(self,view):
        """
        Draws the defense barriers
        """
        if (self._left_barrier != None):
            self._left_barrier.draw(view)
        if(self._right_barrier != None):
            self._right_barrier.draw(view)
    # HELPER METHODS FOR COLLISION DETECTION
    def alien_collisions(self):
        """
        Checks each single in every row and column and determines if it
        has collided with the ship's bolt. If it has, remove that particular alien
        and remove the ship's bolt from _bolt.

        For every removal, it adds 1 to _dead_count
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] != None:
                    for ii in self._bolts:
                        if ii.get_kind_bolt() == 'player':
                            if self._aliens[x][y].detect_bolt_collision(ii):
                                self._aliens[x][y] = None
                                self._bolts.remove(ii)
                                self._exists_player_bolt = False
                                self._dead_count += 1

    def ship_collisions(self):
        """
        Checks if the ship has collided with the aliens' bolt. If it has, remove
        the alien's bolt from _bolt and sets the ship's alive status to False in
        _ship_alive.
        """
        for ii in self._bolts:
            if ii.get_kind_bolt() == 'alien':
                if self._ship.detect_alien_bolt_collision(ii):
                    self._bolts.remove(ii)
                    self._ship_alive = False
                    print("_ship_alive = false")

    def alien_dline_collision(self):
        """
        Checks every alien to see if it has crossed the defensive line
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] != None and \
                self._aliens[x][y].get_alien_y() <= DEFENSE_LINE + ALIEN_HEIGHT/2:
                    self._dline_breached = True


    def barrier_collision(self):
        """
        Check to see if a bolt hits the barrier, sets self._barrier to None when lives hit 0
        """

        for i in self._bolts:
            if(self._left_barrier != None):
                if self._left_barrier.detect_bolt_collision(i):
                    self._left_barrier.decrease_lives()
                    self._bolts.remove(i)
                    if i.get_kind_bolt() == 'player':
                        self._exists_player_bolt = False
            if(self._right_barrier != None):
                if self._right_barrier.detect_bolt_collision(i):
                    self._right_barrier.decrease_lives()
                    self._bolts.remove(i)
                    if i.get_kind_bolt() == 'player':
                        self._exists_player_bolt = False
        if(self._left_barrier != None):
            if self._left_barrier.get_lives() == 0:
                self._left_barrier = None
        if(self._right_barrier != None):
            if self._right_barrier.get_lives() == 0:
                self._right_barrier = None
