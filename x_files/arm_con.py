'''
创建时间:Sun Aug  5 21:02:29 BST 2018
'''

from math import *
import numpy as np

class Arm(object):
    '''to solve angle transform problem'''
    r1 = 0
    r2 = 0
    r3 = 0
    steps = 10

    def __init__(self):
        pass
    
    def t_solve_angle(self, a, b):
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
                if not -half_pi < d2 < half_pi:
                    continue
                d3 = pi - acos((self.r2 ** 2 + self.r3 ** 2 - temp) / (2 * self.r2 * self.r3))
                if not -half_pi < d3 < half_pi:
                    continue
                opt_val = self.opt(d1, d2, d3, self.position)
                if opt_val < s:
                    s = opt_val
                    rs = d1, d2, d3
            except Exception as e:
                print(e)
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
            first_solutions = set(range(-l1 * Arm.steps, m11)).union(set(range(m12, l1 * Arm.steps)))
            second_solutions = set(range(m21, m22)).union(set(range(u, l1 * Arm.steps)))
            return np.array(list(first_solutions.intersection(second_solutions))) / Arm.steps
        else:
            print(0)
            m1 = u
            m2 = -A / (2 * a)
            return np.arange(m1 + Arm.step_length, m2, Arm.step_length)

def main():
    am = Arm()
    out = am.t_solve_angle(23,23)
    print(out)

if __name__ == '__main__':
    main()