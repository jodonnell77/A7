"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# John O'Donnel (jro79) and Anthony Nguyen (an523)
# 4/27/2019
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _lives
    _lives_numlabel
    _pause_message
    _score_label
    _score
    _background
    _infotext
    _pause
    _right_b_hp
    _left_b_hp
    """

    # DO NOT MAKE A NEW INITIALIZER


    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._background =GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,height=GAME_HEIGHT,\
        source='space.png')
        self._wave = None
        self._pause = 0
        self._text = GLabel(text='Press \'s\' to play',halign='center',\
        valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,fillcolor=None,\
        font_name='Arcade',font_size=80, linecolor = "white")

        self._infotext = GLabel(text='BEWARE: Aliens have guided missiles',halign='center',\
        valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2.5,fillcolor=None,\
        font_name='Arcade',font_size=30, linecolor = "white")

        self._lives = PLAYER_LIVES
        self._lives_numlabel = GLabel(text=str(self._lives)+' Lives Left',\
        halign='right',valign='top',x=GAME_WIDTH-25,y=GAME_HEIGHT-25,\
        fillcolor=[1,1,1,1],font_name='Arcade',font_size=40)
        self._pause_message = None
        self._score = 0
        self._left_b_hp = BARRIER_HP
        self._right_b_hp = BARRIER_HP
        self._left_b_label = GLabel(text='L-Barrier HP:'\
        +str(self._left_b_hp), \
        halign='right',valign='top',x=250,y=GAME_HEIGHT-50, \
        fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")
        self._right_b_label = GLabel(text='R-Barrier HP:'\
        +str(self._right_b_hp), \
        halign='right',valign='top',x=400,y=GAME_HEIGHT-50, \
        fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")



    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME

        self.STATE_INACTIVE_Helper()
        self.STATE_NEWWAVE_Helper()
        self.STATE_ACTIVE_Helper(dt)
        self.STATE_PAUSED_Helper()
        self.STATE_CONTINUE_Helper()
        self.STATE_COMPLETE_Helper()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        self._background.draw(self.view)
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
            self._infotext.draw(self.view)
        if self._state == STATE_NEWWAVE:
            self._text = None
        if self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
            self._lives_numlabel.draw(self.view)
            self._score_label.draw(self.view)
            self._miss_label.draw(self.view)
            self._left_b_label.draw(self.view)
            self._right_b_label.draw(self.view)
        if self._state == STATE_PAUSED:
            self._pause_message.draw(self.view)
            self._wave.draw(self.view)
            self._lives_numlabel.draw(self.view)
            self._score_label.draw(self.view)
            self._miss_label.draw(self.view)
            self._left_b_label.draw(self.view)
            self._right_b_label.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._pause_message.draw(self.view)
            self._wave.draw(self.view)
            self._score_label.draw(self.view)
            self._lives_numlabel.draw(self.view)
            self._miss_label.draw(self.view)
            self._left_b_label.draw(self.view)
            self._right_b_label.draw(self.view)



    # HELPER METHODS FOR THE STATES GO HERE
    def STATE_INACTIVE_Helper(self):
        """
        Helper while state is STATE_INACTIVE

        Determines the current state and assigns it to self._state

        This method checks for a key press, and if there is one, changes the state.
        If the user presses 's' key at the welcome screen, changes state to STATE_NEWWAVE""
        """
        #Welcome screen
        if self.input.is_key_down('s') and self._state == STATE_INACTIVE:
            self._state = STATE_NEWWAVE

    def STATE_NEWWAVE_Helper(self):
        """
        Helper while state is STATE_NEWWAVE

        This method creates a wave and changes state to STATE_ACTIVE
        """
        if self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE

    def STATE_ACTIVE_Helper(self, dt):
        """
        Helper while state is STATE_ACTIVE

        This method:
        -Displays the SCORE, PLAYER LIVES, and updates the Wave.
        -Checks if the ship is currently alive and if any alien has
         breached the DEFENSE_LINE.
        -Checks how many aliens have been eliminated. If all aliens have been
         eliminated then the player has won the game
        -Checks if the player has pressed 'P'. If so, pauses the game.
        """
        if(self._state == STATE_ACTIVE):
            #update life if lost a life
            self._lives_numlabel = GLabel(text=str(self._lives)+' Lives',\
            halign='right',valign='top',x=GAME_WIDTH-75,y=GAME_HEIGHT-25,\
            fillcolor=None,font_name='Arcade',font_size=40, linecolor = "white")
            #updates Score #more score is rewarded for less missed shots
            self._score = int(self._wave.get_dead_count()*POINTS_PER_KILL\
            -self._wave.get_missed_shots()*MISS_PENALTY)
            self._score_label = GLabel(text='Score: '+str(self._score),\
            halign='right',valign='top',x=100,y=GAME_HEIGHT-25,\
            fillcolor=None,font_name='Arcade',font_size=40, linecolor = "white")
            self._miss_label = GLabel(text='Misses: '\
            +str(self._wave.get_missed_shots()), \
            halign='right',valign='top',x=75,y=GAME_HEIGHT-50, \
            fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")
            self._wave.update(self._input, dt)
            #Checks if the ship is alive, if ship dies,reduce score by DEATH_PENALTY
            if self._wave.get_ship_alive() == False:
                self._state = STATE_PAUSED
                self._lives -= 1
            if self._wave.get_dline_breached() == True:
                self._state = STATE_COMPLETE
            #if dead count == number of starting aliens,the player has completed the wave
            if self._wave.get_dead_count() == ALIEN_ROWS * ALIENS_IN_ROW:
                self._state = STATE_COMPLETE
            #player input pause
            if self.input.is_key_down('p'):
                self._state = STATE_PAUSED
                self._pause = 1
            self.update_barriers()

    def update_barriers(self):
        if self._wave.get_left_barrier != None:
            self._left_b_hp = self._wave.get_left_barrier_health()
            self._left_b_label = GLabel(text='L-Barrier HP:'\
            +str(self._left_b_hp), \
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT-25, \
            fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")

        if self._wave.get_right_barrier != None:
            self._right_b_hp = self._wave.get_right_barrier_health()
            self._right_b_label = GLabel(text='R-Barrier HP:'\
            +str(self._right_b_hp), \
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT-50, \
            fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")

        if self._wave.get_left_barrier == None:
            self._left_b_hp = 0
            self._left_b_label = GLabel(text='L-Barrier HP:'\
            +str(0), \
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT-25, \
            fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")

        if self._wave.get_right_barrier == None:
            self._right_b_hp = 0
            self._right_b_label = GLabel(text='R-Barrier HP:'\
            +str(0), \
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT-50, \
            fillcolor=None,font_name='Arcade',font_size=20, linecolor = "white")

    def STATE_PAUSED_Helper(self):
        """
        Helper while state is STATE_PAUSED

        If the player is paused and has more than 0 lives, gives the player
        the option to continue the game. If the player presses 's',
         passes the _state to STATE_CONTINUE

        If the player is paused and has 0 lives, passes the _state to STATE_CONTINUE
        """
        if self._state == STATE_PAUSED and self._lives > 0:
            self._pause_message =  GLabel(text="Ship hit: Press 'S' to continue",\
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,\
            fillcolor=None,font_name='Arcade',font_size=40, linecolor = "white")

            if self.input.is_key_down('s') and self._state == STATE_PAUSED:
                self._state = STATE_CONTINUE
                self._wave.set_ship_alive()

        if self._state == STATE_PAUSED and self._pause == 1:
            self._pause_message =  GLabel(text="Paused: Press 'S' to continue",\
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,\
            fillcolor=None,font_name='Arcade',font_size=40, linecolor = "white")

            if self.input.is_key_down('s') and self._state == STATE_PAUSED:
                self._state = STATE_CONTINUE
                self._pause = 0

        if self._state == STATE_PAUSED and self._lives == 0:
            self._state = STATE_CONTINUE

    def STATE_CONTINUE_Helper(self):
        """
        Helper while state is STATE_CONTINUE

        Checks the number of lives the player has. If > 0 lives then sets state to
        STATE_ACTIVE and the player continues the game. If = 0 lives sets the _state
        to STATE_COMPLETE
        """
        if self._state == STATE_CONTINUE and self._lives > 0:
            self._state = STATE_ACTIVE

        if self._state == STATE_CONTINUE and self._lives == 0:
            self._state = STATE_COMPLETE

    def STATE_COMPLETE_Helper(self):
        """
        Helper while state is STATE_COMPLETE

        Displays a message if the player has won the game, ran out of lives, or
        that the aliens have breached the defensive life
        """
        if self._state == STATE_COMPLETE and self._lives == 0:
            self._pause_message =  GLabel(text="YOU RAN OUT OF LIVES!",\
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,\
            fillcolor=None,font_name='Arcade',font_size=40, linecolor = "white")

        if self._state == STATE_COMPLETE and self._lives > 0:
            self._pause_message =  GLabel(text="YOU WIN!",\
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,\
            fillcolor=None,font_name='Arcade',font_size=40, linecolor = "white")
            if self.input.is_key_down('s') and self._state == STATE_COMPLETE:
                self._state == STATE_NEWWAVE

        if self._state == STATE_COMPLETE and self._wave.get_dline_breached() == True:
            self._pause_message =  GLabel(text="THE ALIENS HAVE INVADED!",\
            halign='right',valign='top',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,\
            fillcolor=None,font_name='Arcade',font_size=40,linecolor = "white")
