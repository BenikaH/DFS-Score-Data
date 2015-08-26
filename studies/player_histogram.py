"""
Produces histogram plots for player point distributions.
The main module of the program will print out all player mean scores and
standard deviations, but using this along with that will give a better
visualization on how they are scoring.
"""

from lib.DB import DB
from matplotlib import pyplot as plt
import lib.get_player as get_player
import numpy as np


class GetHist:
    def __init__(self, player_id, site='dk'):
        self.db = DB()
        self.id_ = player_id

        self.points = self.get_points(player_id, site)

    def get_mean(self):
        return np.mean(self.points)

    def get_name(self):
        return get_player.name_from_id(self.id_)

    def get_stdev(self):
        return np.std(self.points)

    def plot_hist(self, bins=20):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.hist(self.points, bins=bins, normed=True)
        self.ax.axvline(self.get_mean(), color='red', linestyle='--', linewidth=1.5,
                        label='Avg. Points: {0:.2f}\nSt. Dev. Points: {1:.2f}'.format(
                            self.get_mean(), self.get_stdev()))
        self.ax.legend(loc='upper right')
        self.ax.set_title(self.get_name())
        self.ax.set_ylabel('%')
        self.ax.set_xlabel('Points Scored')

    def get_points(self, id_, site):
        q = "SELECT {}_pts FROM rguru_hitters WHERE id={}".format(site, id_)
        return [float(x[0]) for x in self.db.query(q)]


class MakePlots:
    """
    Takes a list of player ids and makes necessary plots
    """
    def __init__(self, ids):
        self.plots = []
        self.make_hist(ids)
        self.make_plots()
        self.set_ax_lims()
        plt.show()

    def get_xaxis(self):
        """
        Gets the largest x-axis value among all the charts. Used with set_ax_lims
        :return:
            max of largest x-axis or arbitrary constant
        """
        ax_val = max([player.ax.get_xlim() for player in self.plots], key=lambda x: x[1])[1]
        return max([ax_val, 30])

    def get_yaxis(self):
        """
        See get_axis
        :return:
        """
        ax_val = max([player.ax.get_ylim() for player in self.plots], key=lambda x: x[1])[1]
        return max([ax_val, 0.45]) + 0.05

    def make_hist(self, ids):
        for id_ in ids:
            self.plots.append(GetHist(id_))

    def make_plots(self):
        for player in self.plots:
            if len(player.points) == 0:
                name = get_player.name_from_id(player.id_)
                if name is None:
                    print "No record for player with id: {}".format(player.id_)
                else:
                    print "No scoring data for player: {} (id={})".format(name, player.id_)
            else:
                player.plot_hist(bins=50)

    def set_ax_lims(self):
        """
        Set the axis limits to be uniform among all of the displayed graphs. Because
        matplotlib will auto size the graphs to fit, it will be hard to compare two
        or more players because their graphs can look so differently.
        :return:
        """
        x_val = self.get_xaxis()
        y_val = self.get_yaxis()
        for player in self.plots:
            player.ax.set_ylim([0, y_val])
            player.ax.set_xlim([0, x_val])