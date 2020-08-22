from floatingPointsClasses import windMatrix, Particle
import random
import numpy as np
import cv2


def main():
    seed = 7  # also used for pnoise2
    random.seed(seed)

    x = 750
    y = 750
    size = (x, y)

    numPts = 200  # number of points
    windScale = 1.5  # scales how much the wind affects particles
    decay = 1  # how much velocity decays with every iteration

    rawWind = windMatrix(seed, size)
    rawWind.normalize()
    rawWind.write()

    adjWind = (rawWind.matrix - 0.5) * windScale

    # random distribution
    points = tuple(Particle([random.randint(0, x - 1), y - 1]) for i in range(numPts))

    # middle 20%
    # points = tuple(Particle([round(x / 2) + random.randint(0, round(x/5)), y - 1]) for i in range(numPts))

    # debug grey background
    # cvWorld = np.ones((x, y, 3)) * 100
    cvWorld = np.zeros((x, y, 3))

    for point in points:
        prevPos = (point.x, point.y)
        # decide what kind of loop to use lol
        index = points.index(point)

        # scales the current index to a value from 0 to 1 to facilitate
        # modulating color and thickness
        thicIndex = 1 - (index / numPts)

        while point.y >= 0:
            pos = (point.x, point.y)

            prevLoc = tuple([round(prevPos[0]), round(prevPos[1])])
            loc = tuple([round(pos[0]), round(pos[1])])

            # debug option to help find where points are
            # cv2.circle(cvWorld, loc, 3, (100, 100, 100))

            # inverts thicIndex and then rescales to fit it between 0.25 and 1
            colorIndex = 0.25 + ((1 - thicIndex) * 0.75)

            # debug option to find lines
            # color = (255, 255, 255)
            color = (200 * colorIndex, 255 * colorIndex, 150 * colorIndex)

            thick = round(thicIndex * (y/150)) + 1

            cv2.line(cvWorld, prevLoc, loc, color, thick, lineType=cv2.LINE_AA)

            # idk why this doesn't work but I'll figure it out later
            # cv2.imshow('output', cvWorld)

            prevPos = (point.x, point.y)

            point.step(adjWind, decay=decay)
            point.constrain(size)
            print('Point: ' + str(index) + '(' + str(point.x) + ', ' + str(point.y) + ')')

    cv2.imwrite('output.png', cvWorld)


if __name__ == "__main__":
    main()
