SERIES = ('e6','e12','e24','e48')

VALUES = {'e6' :(100,150,220,330,470,680),
          'e12':(100,120,150,180,220,270,
                 330,390,470,560,680,820),
          'e24':(100,110,120,130,150,160,
                 180,200,220,240,270,300,
                 330,360,390,430,470,510,
                 560,620,680,750,820,910),
          'e48':(100,105,110,115,121,127,
                 133,140,147,154,162,169,
                 178,187,196,205,215,226,
                 237,249,261,274,287,301,
                 316,332,348,365,383,402,
                 442,453,464,487,511,536,
                 562,590,619,649,681,715,
                 750,787,825,866,909,953)}

def normalize_series(series='e12'):
    ''' Normalize series into values 1 .. 10
    Keyword arguments:
        series -- initial series (default e12)
    Return: normalized series (tuple) 
    '''
    if series not in SERIES:
        raise ValueError('unknown value series')
    ext_row = list(VALUES[series])+[VALUES[series][0]*10,]
    return tuple([elem / 100  for elem in ext_row])

''' test '''
print(normalize_series('e6'))
