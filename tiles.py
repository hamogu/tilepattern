import numpy as np
import matplotlib.pyplot as plt

class TilePattern(object):
    tilesize = (5., 19.)
    n_tiles = (22, 32)
    colors = [(.1, .8, .1),(0, .7, .1), (0, 1, .2)]
    offset = np.zeros(n_tiles[1])

    def __init__(self, pattern=None):
        if pattern == None:
            self.pattern = np.random.randint(0, len(self.colors), self.n_tiles)

    def plot(self, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        xcoos, ycoos = np.mgrid[0:self.n_tiles[0], 0:self.n_tiles[1]]
        xcoos = np.asfarray(xcoos)
        xcoos += self.offset[np.newaxis, :]
        for i in set(self.pattern.flatten()):
            ind = (self.pattern == i)
            # stupid mpl bug for height
            height = np.ones(ind.sum()) * self.tilesize[0]
            ax.bar(left=xcoos[ind] * self.tilesize[1],
                   height=height,
                   bottom=ycoos[ind] * self.tilesize[0],
                   width=self.tilesize[1],
                   color=self.colors[i],
                   edgecolor='0.8', linewidth=1)

class StripedPattern(TilePattern):
    p = [.5, .3, .2]
    def __init__(self):
        # This is a delta color array
        self.pattern = np.random.choice(3, size=self.n_tiles, p=self.p)
        # but make start line with equal distribution
        self.pattern[:, 0] = np.random.choice(3, self.n_tiles[0])
        self.pattern = np.cumsum(self.pattern, axis=0)
        self.pattern = np.mod(self.pattern, 3)
