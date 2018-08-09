from math import *
import numpy as np
from numpy.linalg import norm

half_pi = pi / 2

class Arm():
    steps = 10
    step_length = 1 / steps
    default_position = np.array([90, 90, 90, 90, 90, 45], np.int32)
    
    @staticmethod
    def minimum_change(d1, d2, d3, p):
        return norm(90 - (np.rad2deg(np.array([d1, d2, d3])) - p[:3]), ord=2)

    def __init__(self, r1, r2, r3, opt=minimum_change, implementation="ax"):
        """
          :param r1: Length of the first segment
          :param r2: Length of the second segment
          :param r3: Length of the third segment
          :param opt: The optimization function.
          """
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.len = r1 + r2 + r3
        self.position = Arm.default_position.copy()

        # servo degree in radians
        self.rad_pos = np.array(
            [half_pi, half_pi, half_pi, half_pi, half_pi, pi / 4], dtype=np.float64)
        self.opt = opt

    def get_radians(self, x, y, z):
        """
        :param x:
        :param y:
        :param z:
        :return: a list of radians
        """
        distance = norm((x, y, z), ord=2)
        if distance > self.len:
            raise Exception("Too far to reach!")

        d0 = atan2(y, x)
        # if not pi * 0.75 < d0 < -pi * 0.25:
        #     raise Exception("Out of range!")

        d1, d2, d3 = self.solve_three(norm((x, y), ord=2), z)
        return np.array((d0, d1, d2, d3), dtype=np.float64)

    def solve_three(self, a, b):
        """
        :param a: x coordinate in the plane
        :param b: y coordinate in the plane
        :return: a list of degrees
        """

        s = inf
        rs = None
        rg = self.get_m_range(a, b)
        for m in rg:
            try:
                d1 = asin(m / self.r1)
                n = sqrt(self.r1 ** 2 - m ** 2)
                temp = (a - m) ** 2 + (b - n) ** 2
                d2 = half_pi - d1 - acos((self.r2 ** 2 + temp - self.r3 ** 2) / (2 * self.r2 * sqrt(temp))) - atan(
                    (b - n) / (a - m))
                if not half_pi < d2 < pi:
                    continue
                d3 = pi - acos((self.r2 ** 2 + self.r3 ** 2 -
                                temp) / (2 * self.r2 * self.r3))
                if not -half_pi < d3 < half_pi:
                    continue
                opt_val = self.opt(d1, d2, d3, self.position)
                if opt_val < s:
                    s = opt_val
                    rs = d1, d2, d3
            except:
                continue
        return rs

    def get_m_range(self, a, b):
        l1 = self.r1
        l2 = self.r2
        l3 = self.r3

        A = l2 ** 2 + l3 ** 2 - l1 ** 2 - a ** 2 - b ** 2

        temp = a ** 2 + b ** 2
        d1 = 4 * temp * l1 ** 2 - A ** 2

        m11 = 0
        m12 = 0
        m21 = 0
        m22 = 0

        if d1 > 0:
            m11 = int((-A * a - b * sqrt(d1)) / (2 * temp) * Arm.steps)
            m12 = int((-A * a + b * sqrt(d1)) / (2 * temp) * Arm.steps)
            # print(m11, m12)

        B = -A - 2 * l2 * l3
        d2 = 4 * temp * l1 ** 2 - B ** 2

        u = int(B / (2 * a) * Arm.steps)

        if d2 > 0:
            m21 = int((B * a - b * sqrt(d2)) / (2 * temp) * Arm.steps)
            m22 = int((B * a + b * sqrt(d2)) / (2 * temp) * Arm.steps)
            # print(m21, m22)

        # print(u - l1)

        if b != 0:
            first_solutions = set(
                range(-l1 * Arm.steps, m11)).union(set(range(m12, l1 * Arm.steps)))
            second_solutions = set(range(m21, m22)).union(
                set(range(u, l1 * Arm.steps)))
            return np.array(list(first_solutions.intersection(second_solutions))) / Arm.steps
        else:
            print(0)
            m1 = u
            m2 = -A / (2 * a)
            return np.arange(m1 + Arm.step_length, m2, Arm.step_length)

    def goto(self, x, y, z):
        self.rad_pos = self.get_radians(x, y, z)
        self.rad_pos[1] = half_pi - self.rad_pos[1]
        self.rad_pos[2] = self.rad_pos[1] - self.rad_pos[2]
        # self.rad_pos[3] = self.rad_pos[2] - self.rad_pos[3] + half_pi
        self.rad_pos[3] = half_pi - self.rad_pos[3]

        self.rad_pos[0] = self.rad_pos[0] * 180 / pi
        self.rad_pos[1] = self.rad_pos[1] * 180 / pi
        self.rad_pos[2] = self.rad_pos[2] * 180 / pi
        self.rad_pos[3] = self.rad_pos[3] * 180 / pi

        print(self.rad_pos)
        return self.rad_pos
        # self.position = np.concatenate((self.cov_degs(self.rads_to_degs(
        #     self.rad_pos)), self.position[4:]), axis=0).astype(np.int32)

if __name__ == '__main__':

    arm = Arm(130, 130, 120, Arm.minimum_change)
    arm.goto(140,70,60)