#!/usr/bin/env python
# -*- coding: utf-8 -*-

# calculate the distance between two lat-long points using a flat-surface
# formula. Alternatively, use the haversine formula for the great circle distance

from math import asin, atan2, cos, radians, sin, sqrt

# Earth's radius in km (wikipedia)
R = 6371.009

# seems wrong!
def sphericalEarth(f, t):
    # assumes that coordinates are lat-long. returns distance between points in
    # meters

    # convert to radians:
    f_lat, f_long = map(radians, f)
    t_lat, t_long = map(radians, t)
    
    meanLat = (f_lat - t_lat) / 2
    
    dLat = t_lat - f_lat
    dLon = t_long - f_long

    return R * sqrt(pow(dLat, 2) + pow((cos(meanLat) * dLon), 2))


def haversine(f, t):

    f_lat, f_long = map(radians, f)
    t_lat, t_long = map(radians, t)

    dLat = t_lat - f_lat
    dLon = t_long - f_long

    a = sin(dLat/2) * sin(dLat/2) + cos(f_lat) * cos(t_lat) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c
    
def altHaversine(lat1, lon1, lat2, lon2):

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c

if __name__ == "__main__":
    
    a = (52.1695180,4.4703890)
    b = (52.1695120,4.4703160)
    D = haversine(a,b)
    print("a = {0}, b = {1}\ndistance = {2}km ~ {3}m ".format(a, b, D, round(D*1000)))
