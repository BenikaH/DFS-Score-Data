"""
This file will calculate various things about how many at bats players get per
game.

- Abstract -
Players that are platoon players are often priced very cheaply. This is probably
due to the fact that they are not every day players or maybe their overall numbers
are priced instead of their numbers vs the specific hand.

A good example can be seen in the Dodgers outfield. The Dodgers essentially have
two players for one position, alternating starts between Andre Ethier vs right-handed
pitchers and Scott Van Slyke vs left-handed pitchers. Some numbers:

           | avg. price | wOBA vs R | wOBA vs L |
Ethier     |       3300 |      .381 |      .283 |
Van Slyke  |       3400 |      .317 |      .382 |

wOBA - career wOBA numbers vs shown pitch hand.
price - the average Draft Kings price for the season.

What the Dodgers are doing is effectively rostering someone every day with the numbers of
a Jose Bautista (.380 season wOBA/.373 career wOBA) or Andrew McCutchen (.393 season/.383 career),
the drawback being that they have to use 2 roster spots and hope that they don't bring in an
opposite handed pitcher from the bullpen.
    note: the wOBAs listed are not filtered for splits.

Where this concerns us as fantasy players is getting value. Comparing the wOBA of all the players listed,
all of the choices seem to be pretty similar.  But where you're really going to gain value is factoring
in player salaries.  The average salary for Bautista and McCutchen is 5000 and 4850, respectively. This
is a pretty huge difference and would seem to make the Ethier/Van Slyke choice the easy pick.
"""

from lib.DB import DB
import datetime
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt


class TeamGame:
    def __init__(self, team):
        self.team = team
        self.calc_season_abs()
        self.games = {}

    def calc_season_abs(self):
        dates = self.get_dates()
        for date in dates:
            res = self.get_team_abs(date, self.team)
            self.games[date] = self.total_abs(res)

    def get_dates(self):
        db = DB()
        q = "SELECT date FROM rguru_hitters WHERE team = %s"
        res = db.query(q, (self.team,))
        db.finish()
        return set([x[0] for x in res])

    def get_team_abs(self, date, team):
        db = DB()
        q = "SELECT name, AB, BB, HBP FROM rguru_hitters WHERE date=%s and team=%s"
        res = db.query(q, (date, team))
        db.finish()
        return res

    def total_abs(self, res):
        """Totals the at-bats and walks for a game"""
        abs_by_pos = np.zeros((9,))
        num_abs = int(sum([sum(t[1:]) for t in res]))
        all_abs, rem_abs = num_abs//9, num_abs % 9
        abs_by_pos += all_abs
        abs_by_pos[:rem_abs] += 1
        return abs_by_pos


class PlayerAbs:
    def __init__(self, id_):
        self.id_ = id_
        self.avg_abs = self.calc_abs_by_pos()

    def query_data(self):
        db = DB()
        q = "SELECT bat_order, AB, BB, HBP FROM rguru_hitters where id=%s"
        res = db.query(q, (self.id_,))
        db.finish()
        return res

    def calc_abs_by_pos(self):
        raw_data = self.query_data()
        abs_by_ord = defaultdict(list)
        for bat_ord, at_bats, bb, hbp in raw_data:
            abs_by_ord[bat_ord].append(at_bats + bb + hbp)

        ab_avgs = {}
        for k, v in abs_by_ord.items():
            if k == '0':
                continue
            ab_avgs[k] = sum(v) / float(len(v))

        return ab_avgs

    def plot_abs(self):
        x_labels, y = zip(*sorted(self.avg_abs.items()))
        x = np.arange(len(x_labels))
        fig, ax = plt.subplots()
        width = 0.35
        ax.bar(x, y, width=width)
        ax.set_xticks(x+width/2.0)
        ax.set_xticklabels(x_labels)
        plt.show()


pl = PlayerAbs('7747')
pl.plot_abs()