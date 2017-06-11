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


def not_in_undisturbed_window(events, undisturbed_start, undisturbed_end):
    results = []
    for e in events:
        if not e['start_time']:
            # no start/end time
            results.append(e)
        else:
            start = parse_time_with_second(e['start_time'])
            end = parse_time_with_second(e['start_time'])
            ustart = parse_time_without_second(undisturbed_start)
            uend = parse_time_without_second(uend)
            if (start < ustart) or (end > uend):
                results.append(e)
    return results


def parse_time_with_second(time):
    return datetime.strptime(time, '%H:%M:%S')


def parse_time_without_second(time):
    return datetime.strptime(time, '%H:%M')
