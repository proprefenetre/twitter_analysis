#!/usr/bin/env python
# -*- coding: utf-8 -*-

# group entities based on their geographical distance

from distances import haversine as dist

def group(center, radius, places):
    grp = set()

    for p in places:
        if dist(center, p) <= radius:
            grp.add(p)
        else:
            pass

    return grp


            


