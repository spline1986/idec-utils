#!/usr/bin/env python3

import sys
import time
from datetime import datetime


def load_echoareas():
    "Read list of echoareas from config file."
    global echoareas
    f = open("statistic.cfg", "r").read().split("\n")
    echoareas = [line for line in f if len(line) > 0]


def read_echoarea(echoarea):
    "Read echoarea index."
    f = open("echo/{}".format(echoarea), "r").read().split()
    return [msgid for msgid in f if len(msgid) == 20]


def read_message_time(msgid):
    "Read message."
    try:
        return int(open("msg/{}".format(msgid), "r").read().split("\n")[2])
    except ValueError:
        return 0


def make_unixtime(stamp):
    "Return unix timestamp from date in string \"YYYY.MM.DD\"."
    return time.mktime(datetime.strptime(stamp, "%Y.%m.%d").timetuple())


def calculate_count(echoarea, start, end):
    "Return number of messages in the echoarea per time period."
    count = 0
    msgids = read_echoarea(echoarea)
    msgids.reverse()
    start = make_unixtime(start)
    end = make_unixtime(end)
    for msgid in msgids:
        message_time = read_message_time(msgid)
        if message_time >= start and message_time <= end:
            count += 1
        else:
            return count
    return count


def counts(start, end):
    counts = []
    for echoarea in echoareas:
        counts.append({"name": echoarea,
                       "count": calculate_count(echoarea, start, end)})
    return counts


args = sys.argv[1:]
load_echoareas()
for echoarea in counts(args[1], args[2]):
    print("{0:.<19}{1:>5}".format(echoarea["name"], echoarea["count"]))
