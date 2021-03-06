#!/usr/bin/env python
# needed to print the degree symbol

import datetime
import ephem
import math
from optparse import OptionParser
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


class analemma():


    def __init__(self, year=int(time.strftime("%Y")), city="Greenwich Observatory", lon='0.0', lat='51.48', color="r"):
        self.obs = ephem.Observer()
        self.obs.lon = lon
        self.obs.lat = lat
        self.city = city
        self.sun = ephem.Sun()
        self.x = []
        self.y = []
        self.year = year
        self.color = color

    def compute(self):
        obs = self.obs
        for m in range(1, 13):
            for d in range(1, 33): # yeah I know its sloppy but it works
                obs.date = '%d/%d/%d 13:00' % (self.year, m,  d)
                obs.date = ephem.date(ephem.date('%d/%d/%d 13:00' % (self.year, m,  d)) - float(self.obs.lon) * 12 / math.pi * ephem.hour)
                self.sun.compute(obs)
                y = float(100 - float(self.sun.alt) * 100 / math.pi)
                x = float(float(self.sun.az) * 100 / math.pi / 2)
                self.x.append(x)
                self.y.append(y)

    def plot(self):
        plt.plot(self.y, self.x, '%s-' % self.color)
        plt.title('analemma as seen from %s (%.1f latitude)' % (self.city, math.degrees(self.obs.lat)))
        plt.xlabel('azimuth (degrees)')
        plt.ylabel('altitude (degrees)')
        

if __name__ == '__main__':
    today = datetime.date.today()
    parser = OptionParser()
    parser.add_option("--year", dest="year", default=2014, help="year to compute for")
    parser.add_option("--city", dest="city", default='Greenwich Observatory', help="city for output in report")
    parser.add_option("--lon", dest="lon", default='0.0', help="longitude in degrees")
    parser.add_option("--lat", dest="lat", default='51.48', help="latitude in degrees")
    (options, args) = parser.parse_args()

    a = analemma(year=options.year, lon=options.lon, city=options.city, lat=options.lat)
    a.compute()
    a.plot()
    fig1 = plt.gcf()
    #plt.show()
    plt.draw()
    fig1.savefig('%s.png' % options.city, dpi=100)
