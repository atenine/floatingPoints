from fallingPointsClasses import windMatrix, Particle
import random
import math
import numpy as np
import cv2


def main():
    seed = 7  # also used for pnoise2
    random.seed(seed)

    x = 1000
    y = 1000
    size = (x, y)

    numPts = 300
    windScale = 1.5

    rawWind = windMatrix(seed, size)
    rawWind.normalize()
    rawWind.write()

    adjWind = (rawWind.matrix - 0.5) * windScale

    points = tuple(Particle([random.randint(0, x - 1), y - 1]) for i in range(numPts))

    cvWorld = np.zeros((x, y, 3))

    for point in points:
        prevPos = (point.x, point.y)
        #  decide what kind of loop to use lol
        index = points.index(point)
        thick = round((numPts + 1 - index) / 100) + 1

        while point.y >= 0:
            pos = (point.x, point.y)

            prevLoc = tuple([round(prevPos[0]), round(prevPos[1])])
            loc = tuple([round(pos[0]), round(pos[1])])

            #  cv2.circle(cvWorld, loc, 3, (100, 100, 100))
            color = (220 / (thick  / 1.5), 150 / (thick / 1.5), 255 / (thick / 1.5))
            cv2.line(cvWorld, prevLoc, loc, color, thick, lineType=cv2.LINE_AA)

            #  cv2.imshow('output', cvWorld)
            prevPos = (point.x, point.y)

            point.step(adjWind)
            point.constrain(size)
            print('Point: ' + str(index) + '(' + str(point.x) + ', ' + str(point.y) + ')')

    cv2.imwrite('output.png', cvWorld)


if __name__ == "__main__":
    main()
