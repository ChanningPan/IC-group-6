from math import *
import numpy as np
from numpy.linalg import norm

half_pi = pi / 2

class Arm():
    def __init__(self, r1, r2):
        """
          :param r1: Length of the first segment
          :param r2: Length of the second segment
          :param r3: Length of the third segment
          :param opt: The optimization function.
          """
        self.r1 = r1
        self.r2 = r2

    def get_radians(self,x,y,z):
        """
        :param x:
        :param y:
        :param z:
        :return: a list of radians
        """
        distance = norm((x, y, z), ord=2)

        d0 = atan2(y, x)

        d1, d2 = self.solve_two(norm((x, y), ord=2), z)
        if d0 < pi/6 or d0 > 5*pi/6:
            print("d0 out of range , d0 = ",d0)
            return False
        if d1 < 0 or d1 > 5 * pi / 6:
            print("d1 out of range, d1 = ",d1)
            return False
        if d2 < 0 or d2 > half_pi:
            print("d2 out of range, d2 = ",d2)
            return False

        return [d0,d1,d2]
    
    def solve_two(self,a,b):
        cta11 = acos(((self.r1)**2 - (self.r2)**2 + a**2 + b**2) / (2 * self.r1 *norm((a,b),ord=2)))
        cta12 = atan(b/a)

        cta1 = cta11 + cta12

        x1 = self.r1 * cos(cta1)
        y1 = self.r1 * sin(cta1)

        cta2 = atan((y1 - b)/(a - x1))

        return cta1,cta2

    def goto(self, x, y, z):
        self.rad_pos = self.get_radians(x, y, z)
        if self.rad_pos:
            print(self.rad_pos)

            self.rad_pos[0] = self.rad_pos[0] * 180 / pi
            self.rad_pos[1] = self.rad_pos[1] * 180 / pi 
            self.rad_pos[2] = self.rad_pos[2] * 180 / pi 

            print(self.rad_pos)
            return self.rad_pos
        else:
            return False

if __name__ == '__main__':
    arm = Arm(130,110)
    arm.goto(0,70,0)