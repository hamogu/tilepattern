import numpy as np
import matplotlib.pyplot as plt
import pandas.io.data as web

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

class FidelityPattern(TilePattern):
    tickersymbols = ['FIS', 'FLTB', 'FHLC', 'FTEC', 'FENY', 'FNCL', 'FMAT', 'FGL',
                     'ONEQ', 'FCOM', 'FCOR', 'FDHC', 'FDLB',
                     'FTAWX', 'FTBWX', 'FEMBX',
                     'FGEAX', 'FAHDX', 'FIPAX', 'FZAIX', 'FZICX',
                     'FOPAX',
                     'FBCVX', 'FLVEX', 'FVDFX', 'FLPSX', 'FDVLX', 'FEQTX',
                     'FMEIX', 'FDSCX', 'FDCAX', 'FARNX', 'FBGRX', 'FTQGX'
]
    def get_ticker_data(self):
        tickerlist = np.random.choice(self.tickersymbols, replace=False, size=self.n_tiles[0])
        tickerdata = []
        for i in range(self.n_tiles[0]):
            print 'Downloading rate chart for {0} from yahoo! finance'.format(tickerlist[i])
            rate = web.DataReader(tickerlist[i], 'yahoo')
            tickerdata.append(rate)
        return tickerdata

    def rate_to_pattern(self, rate):
        rate = rate['Close'][::len(rate) / self.n_tiles[1]]
        return np.digitize(rate, np.percentile(rate, [30, 70]))[:self.n_tiles[1]]


    def __init__(self, tickerdata=None):
        if tickerdata is None:
            self.tickerdata = self.get_ticker_data()
        else:
            self.tickerdata = tickerdata

        self.pattern = np.zeros(self.n_tiles)
        for i in range(self.n_tiles[0]):
            rate = self.tickerdata[i]
            self.pattern[i, :] = self.rate_to_pattern(rate)
        self.pattern = np.asarray(self.pattern, dtype=int)

class FidelityDiff(FidelityPattern):
    def rate_to_pattern(self, rate):
        ratediff = np.diff(rate['Close'][::len(rate) / self.n_tiles[1]])
        return np.digitize(ratediff, np.percentile(ratediff, [30, 70]))[:self.n_tiles[1]]
