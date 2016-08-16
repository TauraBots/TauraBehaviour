from math import *

class Point2(object):
    """
    This class represents a 2D vector and stores the rectangular and polar 
    coordinates at the same time avoiding the need of convertion
    """
    def __init__(self, x=None, y=None, phi=None, r=None, a=None, 
        rectCoords=None, polarCoords=None, vector=None):
        """All the parameters are optional. Examples of usage of Point2 
        constructor and its results (where r(x, y) are rectangular coordinates
         and p(r, a) are polar coordinates:
        # No arguments
        >>> Point2()
        r(0, 0) p(0, 0)

        # only phi
        >>> Point2(phi=1)
        r(0, 0) p(0, 0)
        >>> Point2(phi=1).phi
        1

        # x and y
        >>> Point2(x=10, y=10)
        r(10, 10) p(14.142135623730951, 0.7853981633974483)

        # radius and angle
        >>> Point2(r=10, a=10)
        r(-8.390715290764524, -5.440211108893697) p(10, 10)

        # (x, y) tuple
        >>> Point2(rectCoords=(10,10))
        r(10, 10) p(14.142135623730951, 0.7853981633974483)

        # (r, a) tuple
        >>> Point2(polarCoords=(10,10))
        r(-8.390715290764524, -5.440211108893697) p(10, 10)

        # nameless x and y
        >>> Point2(1,2)
        r(1, 2) p(2.23606797749979, 1.1071487177940904)

        # another vector
        >>> v = Point2(1,2)
        >>> v
        r(1, 2) p(2.23606797749979, 1.1071487177940904)
        >>> Point2(vector=v)
        r(1, 2) p(2.23606797749979, 1.1071487177940904)"""
        self.__dict__['x'] = 0.0
        self.__dict__['y'] = 0.0
        self.__dict__['r'] = 0.0
        self.__dict__['a'] = 0.0
        self.__dict__['phi'] = 0.0
        if not x==None and not y==None:
            self.__dict__['x'] = x
            self.__dict__['y'] = y
            self.__dict__['r'] = sqrt(self.x**2 + self.y**2)
            self.__dict__['a'] = atan2(self.y, self.x)
        elif not r==None and not a==None:
            self.__dict__['r'] = r
            self.__dict__['a'] = a
            self.__dict__['x'] = self.r * cos(self.a)
            self.__dict__['y'] = self.r * sin(self.a)
        elif rectCoords:
            self.__dict__['x'] = rectCoords[0]
            self.__dict__['y'] = rectCoords[1]
            self.__dict__['r'] = sqrt(self.x**2 + self.y**2)
            self.__dict__['a'] = atan2(self.y, self.x)
        elif polarCoords:
            self.__dict__['r'] = polarCoords[0]
            self.__dict__['a'] = polarCoords[1]
            self.__dict__['x'] = self.r * cos(self.a)
            self.__dict__['y'] = self.r * sin(self.a)
        elif vector:
            self.__dict__['x'] = vector.x
            self.__dict__['y'] = vector.y
            self.__dict__['r'] = vector.r
            self.__dict__['a'] = vector.a
            self.__dict__['phi'] = vector.phi
        if phi:
            self.__dict__['phi'] = phi

    def recalc(self, fromRect=True):
        """Used internally to recalculate the values of one set of coordinates 
        when the other is changed."""
        if fromRect:
            self.__dict__['r'] = sqrt(self.x**2 + self.y**2)
            self.__dict__['a'] = atan2(self.y, self.x)
        else:
            self.__dict__['x'] = self.r * cos(self.a)
            self.__dict__['y'] = self.r * sin(self.a)
        return self

    def setCoords(self, coords, isRect=True):
        """Sets coordinates using a tuple. By default the tuple is interpreted 
        as rectangulars coordinates unless you tell that `isRect` is `false`"""
        if isRect:
            self.x = coords[0]
            self.y = coords[1]
            self.recalc()
        else:
            self.r = coords[0]
            self.a = coords[1]
            self.recalc(False)
        return self

    def setX(self, x):
        """Sets self.x to x and recalculates the other coordinates."""
        self.x = x
        self.recalc()
        return self

    def setY(self, y):
        """Sets self.y to y and recalculates the other coordinates."""
        self.y = y
        self.recalc()
        return self

    def setR(self, r):
        """Sets self.r to r and recalculates the other coordinates."""
        self.r = r
        self.recalc()
        return self

    def setA(self, a):
        """Sets self.a to a and recalculates the other coordinates."""
        self.a = a
        self.recalc()
        return self

    def getCoords(self, isRect=True, getPhi=False):
        """Returns a tuple with two rectangular coordinates if `isRect` is True 
        or two polar coordinates if `isRect` is False. If `getPhi` is True it 
        returns three coordinates, the last one being the value of phi."""
        if isRect:
            if getPhi:
                return (self.x, self.y, self.phi)
            return (self.x, self.y)
        else:
            if getPhi:
                return (self.r, self.a, self.phi)
            return (self.r, self.a)

    def zero(self):
        """Makes all of the coordinates equals to zero (including phi)"""
        self.__dict__['x'] = 0
        self.__dict__['y'] = 0
        self.__dict__['r'] = 0
        self.__dict__['a'] = 0
        self.__dict__['phi'] = 0

    def __setattr__(self, name, value):
        """Point2.x, Point2.y, Point2.r, Point2.a, Point2.phi -> number

        Accesses any of the member variables of Point2 to set and get them
        directly. Exemples:
        v.x = 2
        x = v.x"""
        if name == 'x' or name == 'y':
            self.__dict__[name] = value
            self.recalc()
        elif name == 'r' or name == 'a':
            self.__dict__[name] = value
            self.recalc(False)
        else:
            self.__dict__[name] = value

    def __iadd__(self, other):
        """Implements the += operation"""
        x = self.x + other.x
        y = self.y + other.y
        return Point2(x,y)

    def __isub__(self, other):
        """Implements the -= operation"""
        x = self.x - other.x
        y = self.y - other.y
        return Point2(x,y)

    def __add__(self, other):
        """Implements the + operation"""
        x = self.x + other.x
        y = self.y + other.y
        return Point2(x,y)

    def __sub__(self, other):
        """Implements the - operation"""
        x = self.x - other.x
        y = self.y - other.y
        return Point2(x,y)

    def __mul__(self, value):
        """Implements the dot (scalar) product for a vector"""
        r = self.__dict__['r'] = self.r * value
        a = self.a
        return Point2(r=r, a=a)

    def __len__(self):
        """Makes possible to call len(vector) to get the length of 
        the vector"""
        return int(self.r)

    def __repr__(self):
        """Returns a string in a 'r(x, y) p(r, a)' format"""
        return "(rect({0}, {1}), polar({2}, {3}), phi({4}))".format( 
            str(self.x), str(self.y), str(self.r), str(self.a), str(self.phi)
        )