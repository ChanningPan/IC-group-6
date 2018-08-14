from start import *

arm = Arm()
arm.connect()
while True:
    arm.goto(100,200,-100)
    arm.goto(-100,200,-100)