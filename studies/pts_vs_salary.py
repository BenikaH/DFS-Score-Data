"""
The purpose of this program is to show the relationship between a players salary
and his points obtained.  I think it can be used to:
    1. Set a benchmark for points needed when targeting a player at a given
    salary.
    2. Find any price points that might be inefficient.
        - If there is any salary that is severely above or below the trend
        line then it would probably be a good salary to avoid or target, respectively.
        As the results would have it, all of the salaries seemed to fall pretty
        close to the trend line, showing that DraftKings has their players
        priced pretty accurately.
        Note: The two outliers at the end of the avg points plot are likely so
        far off due to a small sample size of players at that salary.  
"""

from lib.DB import DB
import matplotlib.pyplot as plt
import numpy as np

def fetch_data(site, pos):
    db = DB()
    q = "SELECT {0}_pts, {0}_salary FROM rguru_{1}".format(site, pos)
    points = []
    salaries = []
    for pts, sal in db.query(q):
        if pts is None or pts < 0 or sal is None or sal == 0:
            continue
        points.append(float(pts))
        salaries.append(float(sal)/1000)

    return salaries, points

def calc_correlation(x, y):
    return np.corrcoef(x, y)[0,1]

def make_reg(x, y):
    line = np.polyfit(x, y, 1)
    return line, np.poly1d(line)

def plot_all(x, y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    eq, reg_func = make_reg(x, y)
    corr = calc_correlation(x, y)
    ax.plot(x, y, 'bo', x, reg_func(x), '-r')
    ax.text(5, 50, 'y = {0:.3f}x + {1:.2f}\nr = {2:.3f}'.format(eq[0], eq[1], corr))
    ax.set_xlabel('Salary (k)')
    ax.set_ylabel('Points')

def make_bins(spacing, min, max):
    return {x/1000.0:[] for x in range(min, max+spacing, spacing)}

def group_points(x, y, bins):
    for sal, pts in zip(x, y):
        for bin_val in sorted(bins):
            if sal <= bin_val:
                bins[bin_val].append(pts)
                break
    return bins

def avg_points(pts_in_bins):
    new_dict = {}
    for k, v in pts_in_bins.items():
        new_dict[k] = np.mean(v)
    return new_dict

def plot_avg(x, y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bins = make_bins(300,2000,7000)
    grouped = group_points(x, y, bins)
    avg = avg_points(grouped)
    sal, pts = zip(*sorted(avg.items()))
    eq, reg_func = make_reg(sal, pts)
    corr = calc_correlation(sal, pts)
    ax.plot(sal, pts, 'bo', sal, reg_func(sal), '-r')
    ax.text(5, 20, 'y = {0:.3f}x + {1:.2f}\nr = {2:.3f}'.format(eq[0], eq[1], corr))
    ax.set_xlabel('Salary (k)')
    ax.set_ylabel('Points')

def main():
    x, y = fetch_data('dk', 'hitters')
    # fig = plt.figure()
    plot_all(x, y)
    plot_avg(x, y)
    plt.show()

main()