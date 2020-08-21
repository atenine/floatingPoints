import noise
import numpy as np
import cv2


class Particle:

    def __init__(self, location):
        """
        Creates a new particle at the specified location, in the format [y, x]
        """
        self.y = location[1]
        self.x = location[0]
        self.yvel = 0.0
        self.xvel = 0.0

    def step(self, wind, fallspeed=-1):
        """
        "Nudges" the falling particle in a certain direction, given by wind in
        format [y, x] and by fallspeed (negative is down)
        """
        pos = (self.x, self.y)
        dx = self.getWindAt(pos, wind)

        self.yvel = max(self.yvel + fallspeed, -10)
        self.xvel += dx

        self.y += self.yvel
        self.x += self.xvel

    def constrain(self, screenSize):
        # screenSize is of format [y, x]

        if self.x >= screenSize[0] or self.x <= 0:
            self.y = -1

    def getWindAt(self, pos, wind):
        """
        Returns the wind at a location in [y, x]
        """
        return wind[int(pos[0]), int(pos[1])]


class windMatrix:

    def __init__(self, seed, size, scale=90.0, octaves=6, persistence=0.5,
                 lacunarity=2):
        """
        Creates a new matrix of perlin noise using noise.pnoise2, and the given
        arguments, where size is [y, x]
        """
        self.matrix = np.zeros(size)
        for y in range(size[1]):
            for x in range(size[0]):
                self.matrix[x][y] = noise.pnoise2(y/scale,
                                                  x/scale,
                                                  octaves=octaves,
                                                  persistence=persistence,
                                                  lacunarity=lacunarity,
                                                  repeatx=x,
                                                  repeaty=y,
                                                  base=seed)

    def normalize(self):
        """
        Normalizes all values in the matrix using z-scores
        """
        max = np.amax(self.matrix)
        min = np.amin(self.matrix)

        self.matrix = ((self.matrix - min) / (max - min))

    def write(self, pathname='wind.png'):
        """
        Writes the image to disk as .png with given filename
        """
        cv2.imwrite(pathname, self.matrix * 255)
