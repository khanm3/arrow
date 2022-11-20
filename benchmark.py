from __future__ import print_function

import sys
from datetime import datetime
from time import time

import arrow
import pytz


def get_local_utc_offset():
    ts = time()
    return (
        datetime.fromtimestamp(ts) - datetime.utcfromtimestamp(ts)
    ).total_seconds() / 60


RFC3339_DATE = '2016-07-18'
RFC3339_TIME = '12:58:26.485897-02:00'
RFC3339_DATE_TIME = RFC3339_DATE + 'T' + RFC3339_TIME

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
DATETIME_OBJ = datetime.strptime(RFC3339_DATE_TIME[:-6], DATE_TIME_FORMAT)\
    .replace(tzinfo=pytz.FixedOffset(get_local_utc_offset() * -1))
TIME = time()


def benchmark_parse():
    def _arrow():
        return arrow.get(RFC3339_DATE_TIME)

    return (_arrow,)


def benchmark_format():

    arr = arrow.get(RFC3339_DATE_TIME)

    def _arrow():
        return arr.isoformat()

    return (_arrow,)


def benchmark_utcnow():
    def _arrow():
        return arrow.utcnow()

    return (_arrow,)


def benchmark_now():
    def _arrow():
        return arrow.now()

    return (_arrow,)


def benchmark_fromtimestamp():
    def _arrow():
        return arrow.Arrow.fromtimestamp(TIME)
    return (_arrow,)


def benchmark_utcfromtimestamp():
    def _arrow():
        return arrow.Arrow.utcfromtimestamp(TIME)
    return (_arrow,)

if __name__ == '__main__':
    import timeit

    benchmarks = [
        benchmark_parse,
        benchmark_format,

        benchmark_utcnow,
        benchmark_now,

        benchmark_fromtimestamp,
        benchmark_utcfromtimestamp,
    ]
    test_only = False

    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        test_only = True

    print('Executing benchmarks ...')

    for k in benchmarks:
        print('\n============ %s' % k.__name__)
        mins = []

        for func in k():
            if test_only:
                print(func.__name__, func())
            else:
                times =\
                    timeit.repeat('func()', setup='from __main__ import func', number=100000)
                t = min(times)
                mins.append(t)

                print(func.__name__, t, times)