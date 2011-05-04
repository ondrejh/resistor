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

def get_multiple(value):
    ''' Get value multiple
          1 for 1 .. 10
          0.1 for 0.1 .. 1
          100 for 100 .. 1000
    Keyword arguments:
        value -- input value
    Rerutn: multiple value (int)
    '''

    multiples = [10**(enum-3) for enum in range(13)]

    if value<multiples[0]: raise ValueError('value out of range (too low)')

    lesthan = [value<enum for enum in multiples]
    if True in lesthan: return multiples[lesthan.index(True)-1]

    raise ValueError('value out of range (too high)')
    
''' test '''
print(get_multiple(9.7))
print(get_multiple(8))
print(get_multiple(100000000))
print(get_multiple(0.02))
