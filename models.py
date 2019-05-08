"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

# John O'Donnel (jro79) and Anthony Nguyen (an523)
# 4/27/2019
"""
from consts import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_ship_x(self):
        """
        Getter for the x position of the Ship
        """
        return self.x
    # INITIALIZER TO CREATE A SHIP
    def __init__(self,a,b,source):
        """
        This method initializes a Ship

        Parameter: a - x position of the ship
        Precondition: a must be an int > 0

        Parameter: b - y position of the ship
        Precondition: b must be an int > 0

        Parameter: source - image file of the ship
        Precondition: source must be a string referencing a valid image file
        """

        super().__init__(x=a,y=b,width=SHIP_HEIGHT,height=SHIP_HEIGHT,source=source)
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move_ship(self,direction):
        """
         This method changes the ships horizontal position
        Parameter: direction - which way will the ship move left or right
        Precondition: direction must be a string of either 'left' or 'right'
        """
        assert isinstance(direction, str)
        assert direction == 'left' or direction == 'right'
        self.stay_on_screen()
        if direction == 'left':
            self.x -= SHIP_MOVEMENT
        elif direction == 'right':
            self.x += SHIP_MOVEMENT

    def stay_on_screen(self):
        """
        Prevents the ship from moving off sceen by moving ship counter to user
        input if the ship is at the bounds of the game window
        """
        if self.x <= 0 + SHIP_WIDTH/2:
            self.x += SHIP_MOVEMENT
        if self.x >= GAME_WIDTH- SHIP_WIDTH/2:
            self.x -= SHIP_MOVEMENT

    def detect_alien_bolt_collision(self,bolt):
        """
        This method checks to see if an bolt fired from the ship has struck an alien if that is true it will
        return True otherwise it will return False

        Parameter bolt: an instance of Class Bolt
        Precondition: bolt is of class bolt
        """

        # [x,y]
        top_left_bolt = [bolt.get_bolt_x() - BOLT_WIDTH/2 , bolt.get_bolt_y() + BOLT_HEIGHT/2]
        top_right_bolt = [bolt.get_bolt_x() + BOLT_WIDTH/2 , bolt.get_bolt_y() + BOLT_HEIGHT/2]
        bottom_left_bolt = [bolt.get_bolt_x() - BOLT_WIDTH/2 , bolt.get_bolt_y() - BOLT_HEIGHT/2]
        bottom_right_bolt =[bolt.get_bolt_x() + BOLT_WIDTH/2 , bolt.get_bolt_y() - BOLT_HEIGHT/2]

        if self.contains((top_left_bolt[0],top_left_bolt[1])):
            return True
        if self.contains((top_right_bolt[0],top_right_bolt[1])):
            return True
        if self.contains((bottom_left_bolt[0],bottom_left_bolt[1])):
            return True
        if self.contains((bottom_right_bolt[0],bottom_right_bolt[1])):
            return True

        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_alien_x(self):
        """
        Getter for the x position of the Alien
        """
        return self.x

    def get_alien_y(self):
        """
        Getter for the y position of the Alien
        """
        return self.y

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,a,b,source):
        """
        Initializes an alien GImage with a given x coordinate, y coordinate, and source file

        Parameter a: x coordinate of the alien
        Precondition: a is an int or float

        Parameter b: y coordinate of the alien
        Precondition: b is an int or float

        Parameter source: image file of the alien
        Precondition: source is a string of the image file's name
        """
        #assert is_instance(a,int) or is_instance(a,float)
        #assert is_instance(b,int) or is_instance(b,float)
        #assert is_instance(source,str)
        #assert source in ALIEN_IMAGES
        super().__init__(x=a,y=b,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=source)


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    def detect_bolt_collision(self,bolt):
        """
        This method checks to see if an bolt fired from the ship has struck an alien if that is true it will
        return True otherwise it will return False

        Parameter bolt: an instance of Class Bolt
        Precondition: bolt is of class bolt
        """

        # [x,y]
        top_left_bolt = [bolt.get_bolt_x() - BOLT_WIDTH/2 , bolt.get_bolt_y() + BOLT_HEIGHT/2]
        top_right_bolt = [bolt.get_bolt_x() + BOLT_WIDTH/2 , bolt.get_bolt_y() + BOLT_HEIGHT/2]
        bottom_left_bolt = [bolt.get_bolt_x() - BOLT_WIDTH/2 , bolt.get_bolt_y() - BOLT_HEIGHT/2]
        bottom_right_bolt =[bolt.get_bolt_x() + BOLT_WIDTH/2 , bolt.get_bolt_y() - BOLT_HEIGHT/2]

        if self.contains((top_left_bolt[0],top_left_bolt[1])):
            return True
        if self.contains((top_right_bolt[0],top_right_bolt[1])):
            return True
        if self.contains((bottom_left_bolt[0],bottom_left_bolt[1])):
            return True
        if self.contains((bottom_right_bolt[0],bottom_right_bolt[1])):
            return True

        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        _kind: The kind of bolt (str) ['player' or 'alien']

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_kind_bolt(self):
        return self._kind

    def get_bolt_y(self):
        return self.y

    def get_bolt_x(self):
        return self.x
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x_pos, y_pos, velocity, kind, fillcolor = 'red'):
        """
        Initializer for the Bolt Class

        Parameter: x_pos is the x position of the Bolt
        Precondition: x_pos is an int or float > 0

        Parameter: y_pos is the y position of the Bolt
        Precondition: y_pos is an int or float > 0

        Parameter: velocity is the speed of the bolt
        Precondition: velocity is an int or float > 0

        Parameter: kind is the type of bolt
        Precondition: kind is a string of either "alien" or "player"

        Parameter: fillcolor is the color of the bolt
        Precondition: fillcolor is a string referencing a valid color
        """
        self._velocity = velocity
        self._kind = kind
        super().__init__(x = x_pos, y=y_pos, width = BOLT_WIDTH, \
        height = BOLT_HEIGHT, fillcolor=fillcolor)
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def move_bolt_up(self):
        """
        Changes the y position of the ship at a rate positive self._velocity
        """
        self.y += self._velocity

    def move_bolt_down(self):
        """
        Changes the y position of the ship at a rate negative self._velocity
        """
        self.y -= self._velocity

    def move_bolt_side(self, x_velocity):
        """
        Changes the x position of the ship
        """
        self.x += x_velocity

class Barrier(GRectangle):
    """
    A class representing a defense barrier

    This barrier does not move the only attribute that matters is it health which starts at 10
    and it decreases by one every time it is hit. At 0 it disappears and leaves the ship
    defensless.

    INSTANCE ATTRIBUTES:
        _lives: Number of lives left [int >= 0]
    """
    def get_lives(self):
        return self._lives
    def decrease_lives(self):
        self._lives -= 1

    def __init__(self,x_pos,y_pos,height,width,lives,fillcolor="green"):
        self._lives = lives
        super().__init__(x=x_pos,y=y_pos,fillcolor=fillcolor, width=width,height=height)

    def detect_bolt_collision(self,bolt):
        """
        This method checks to see if an bolt fired from the ship has struck an alien if that is true it will
        return True otherwise it will return False

        Parameter bolt: an instance of Class Bolt
        Precondition: bolt is of class bolt
        """

        # [x,y]
        top_left_bolt = [bolt.get_bolt_x() - BOLT_WIDTH/2 , bolt.get_bolt_y() + BOLT_HEIGHT/2]
        top_right_bolt = [bolt.get_bolt_x() + BOLT_WIDTH/2 , bolt.get_bolt_y() + BOLT_HEIGHT/2]
        bottom_left_bolt = [bolt.get_bolt_x() - BOLT_WIDTH/2 , bolt.get_bolt_y() - BOLT_HEIGHT/2]
        bottom_right_bolt =[bolt.get_bolt_x() + BOLT_WIDTH/2 , bolt.get_bolt_y() - BOLT_HEIGHT/2]

        if self.contains((top_left_bolt[0],top_left_bolt[1])):
            return True
        if self.contains((top_right_bolt[0],top_right_bolt[1])):
            return True
        if self.contains((bottom_left_bolt[0],bottom_left_bolt[1])):
            return True
        if self.contains((bottom_right_bolt[0],bottom_right_bolt[1])):
            return True

        return False
