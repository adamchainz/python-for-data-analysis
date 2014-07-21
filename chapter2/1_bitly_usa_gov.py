# coding=utf-8
import json
from pandas import DataFrame, Series
import numpy as np


def main():
    path = '1_usagov_bitly_data2012-03-16-1331923249.txt'
    records = [json.loads(line) for line in open(path)]
    frame = DataFrame(records)

    tz_counts = frame['tz'].value_counts()
    print "Top timezones:"
    print tz_counts[:10]
    print ""

    clean_tz = frame['tz'].fillna('Missing')
    clean_tz[clean_tz == ''] = 'Unknown'
    tz_counts2 = clean_tz.value_counts()
    print "Cleaned top timezones:"
    print tz_counts2[:10]
    print ""

    agents = Series([x.split()[0] for x in frame['a'].dropna()])
    print "Top User Agents:"
    print agents.value_counts()[:10]
    print

    cframe = frame[frame['a'].notnull()]
    operating_system = np.where(
        cframe['a'].str.contains('Windows'),
        'Windows',
        'Not Windows'
    )
    by_timezone_os = cframe.groupby(['tz', operating_system])
    agg_counts = by_timezone_os.size().unstack()
    agg_counts.fillna(0, inplace=True)
    timezone_totals = agg_counts.sum(1).argsort()
    count_subset = agg_counts.take(timezone_totals)[-10:]
    print "OS split by top timezones by counts:"
    print count_subset
    print ""

if __name__ == '__main__':
    main()
