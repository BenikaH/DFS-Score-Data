from lib.DB import DB

class GetBuckets:
    def __init__(self, player_id, spacing=5, max=20, site='dk'):
        self.buckets = self.set_spacing(spacing, max)
        self.db = DB()

        self.points = self.get_points(player_id, site)

    def make_freqs(self, points):
        max_key = max(self.buckets.keys())
        for pt in points:
            for bucket in sorted(self.buckets.keys()):
                if pt <= bucket:
                    self.buckets[bucket] += 1
                    break
                elif pt > max_key:
                    self.buckets[max_key] += 1
                    break

    def make_hist(self):
        height = max(self.buckets.values())
        table = [[' ' for x in range(len(self.buckets.keys()))] for y in range(height)]
        for row in range(len(table)):
            for n, col in enumerate([v for k, v in sorted(self.buckets.items())]):
                if col - 1 >= row:
                    table[row][n] = 'x'

        return list(reversed(table))

    def print_table(self, table):
        for n, row in enumerate(table):
            print str(len(table) - n).zfill(2), row

    def set_spacing(self, spacing, max=20):
        return {x: 0 for x in range(0, max+1, spacing)}

    def get_points(self, id_, site):
        q = "SELECT {}_pts FROM rguru_hitters WHERE id={}".format(site, id_)
        return [float(x[0]) for x in self.db.query(q)]

b = GetBuckets(7513)
b.make_freqs(b.points)
b.print_table(b.make_hist())