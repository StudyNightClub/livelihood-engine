# encoding: utf-8

from datetime import datetime
import sys
import haversine


DISTANCE = 0.300  # 300 m


def nearby_events(events, lat, lon):
    results = []
    for e in events:
        if get_min_distance(e, lat, lon) < DISTANCE:
            results.append(e)
    return results


def get_min_distance(event, lat, lon):
    min_dist = sys.float_info.max
    for area in event['affected_areas']:
        for coord in area['coordinates']:
            dist = haversine.distance(coord['wgs84_latitude'],
                    coord['wgs84_longitude'], lat, lon)
            min_dist = min(min_dist, dist)
    return min_dist
