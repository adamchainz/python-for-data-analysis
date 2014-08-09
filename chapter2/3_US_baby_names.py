#!/usr/bin/env python
import zipfile

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    columns = ['name', 'sex', 'births']
    pieces = []
    nameszip = zipfile.ZipFile('./names.zip', 'r')
    for name in nameszip.namelist():
        if name.startswith('yob'):
            year = int(name[3:7])
            frame = pd.read_csv(nameszip.open(name), names=columns)
            frame['year'] = year
            pieces.append(frame)

    names = pd.concat(pieces, ignore_index=True)

    total_births = names.pivot_table('births', rows='year',
                                     cols='sex', aggfunc=sum)

    print "Total births data:"
    print total_births.head(10)

    def add_prop(group):
        # prop = proportion
        # Integer division would floor...
        births = group.births.astype(float)
        group['prop'] = births / births.sum()
        return group
    names = names.groupby(['year', 'sex']).apply(add_prop)

    print ""
    print "Births with proportions added:"
    print names.head(10)

    assert np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

    def get_top_1000(group):
        return group.sort_index(by='births', ascending=False)[:1000]
    grouped = names.groupby(['year', 'sex'])
    top_1000 = grouped.apply(get_top_1000)

    print ""
    print "Top 1000 names:"
    print top_1000.head(10)

    boys = top_1000[top_1000.sex == 'M']
    # girls = top_1000[top_1000.sex == 'F']

    total_births = top_1000.pivot_table('births', rows='year',
                                        cols='name', aggfunc=sum)

    print ""
    print "Top total births:"
    print total_births.head(10)

    subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
    subset.plot(subplots=True, figsize=(12, 10), grid=False,
                title="Number of births per year")
    plt.show()

    table = top_1000.pivot_table('prop', rows='year', cols='sex', aggfunc=sum)
    table.plot(title='Sum of table1000.prop by year and sex',
               yticks=np.linspace(0, 1.2, 1.3), xticks=range(1880, 2020, 10))
    plt.show()

    print ""
    boys_2010 = boys[boys['year'] == 2010]
    print "Num names in top 50 perecent in 2010: ", quantile_count(boys_2010)
    print ""
    boys_1900 = boys[boys['year'] == 1900]
    print "Num names in top 50 perecent in 1900: ", quantile_count(boys_1900)

    diversity = (
        top_1000.groupby(['year', 'sex']).apply(quantile_count).unstack('sex')
    )

    print ""
    print "Diversity table:"
    print diversity.head(10)

    diversity.plot(title="Number of popular names in top 50%")
    plt.show()

    get_last_letter = lambda x: x[-1]
    last_letters = names['name'].map(get_last_letter)
    last_letters.name = 'last_letter'
    table = names.pivot_table('births', rows=last_letters,
                              cols=['sex', 'year'], aggfunc=sum).fillna(0)

    subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
    print ""
    print "Last letters for select years"
    print subtable.head(10)

    letter_prop = subtable / subtable.sum().astype(float)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
    letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',
                          legend=False)
    plt.show()

    letter_prop = table / table.sum().astype(float)
    dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
    print ""
    print "Male names ending d/n/y trends:"
    print dny_ts.head()

    dny_ts.plot()
    plt.show()

    all_names = top_1000['name'].unique()
    mask = np.array(['lesl' in x.lower() for x in all_names])
    lesley_like = all_names[mask]
    print ""
    print "Lesley-like names:"
    print lesley_like

    filtered = top_1000[top_1000['name'].isin(lesley_like)]
    print "Total Lesley-like births:"
    print filtered.groupby('name')['births'].sum()

    table = filtered.pivot_table('births', rows='year', cols='sex',
                                 aggfunc=sum)
    table = table.div(table.sum(1), axis=0).fillna(0)
    print ""
    print "proportion of Lesley-like names in a given year"
    print table.tail(10)

    table.plot(style={'M': 'k-', 'F': 'k--'})
    plt.show()


def quantile_count(group, q=0.5):
    prop_cumsum = group.sort_index(by='prop', ascending=False)['prop'].cumsum()
    return prop_cumsum.values.searchsorted(q) + 1


if __name__ == '__main__':
    main()
