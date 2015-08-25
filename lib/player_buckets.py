from lib.DB import DB
from matplotlib import pyplot as plt
import get_player


class GetBuckets:
    def __init__(self, player_id, site='dk'):
        self.db = DB()
        self.id_ = player_id

        self.points = self.get_points(player_id, site)

    def get_name(self):
        return get_player.name_from_id(self.id_)

    def plot_hist(self, bins=20):
        fig = plt.figure()
        plot = fig.add_subplot(111)
        plot.hist(self.points, bins=bins, normed=True)
        av_points = sum(self.points)/len(self.points)
        plot.axvline(av_points, color='red', linestyle='--', linewidth=1.5,
                     label='Avg. Points: {0:.2f}'.format(av_points))
        plot.legend(loc='upper right')
        plot.set_title(self.get_name())
        plot.set_ylabel('%')
        plot.set_xlabel('Points Scored')

    def get_points(self, id_, site):
        q = "SELECT {}_pts FROM rguru_hitters WHERE id={}".format(site, id_)
        return [float(x[0]) for x in self.db.query(q)]


def make_plots(ids):
    for id_ in ids:
        player_data = GetBuckets(id_)
        if len(player_data.points) == 0:
            name = get_player.name_from_id(999)
            if name is None:
                print "No record for player with id: {}".format(id_)
            else:
                print "No scoring data for player: {} (id={})".format(name, id_)
        else:
            player_data.plot_hist(bins=50)

    plt.show()