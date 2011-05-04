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
    Return: normalized series (list) 
    '''
    if series not in SERIES:
        raise ValueError('unknown value series')
    ext_row = list(VALUES[series])+[VALUES[series][0]*10,]
    return [elem / 100  for elem in ext_row]

def get_multiple(value):
    ''' Get normalized value multiple
    Keyword arguments:
        value -- input value
    Rerutn: multiple value (int)
          1 for 1 .. 10
          0.1 for 0.1 .. 1
          100 for 100 .. 1000
    '''
    multiples = [10**(enum-3) for enum in range(13)]
    if value<multiples[0]: raise ValueError('value out of range (too low)')
    lesthan = [value<enum for enum in multiples]
    if True in lesthan: return multiples[lesthan.index(True)-1]
    raise ValueError('value out of range (too high)')

def get_nearest_in_series(value,series='e12'):
    ''' Get nearest value in defined series
    Keyword arguments:
        value -- input value
        series -- defined series ('e12' default)
    Return: Nearest value in series
    '''
    if value==0: raise ValueError('non 0 value expected')
    mult = get_multiple(value)
    norm = [enum*mult for enum in normalize_series(series)]
    errs = [abs(enum-value)/value for enum in norm]
    return norm[errs.index(min(errs))]

def get_divider(div,series='e12',mult=100):
    ''' Get the best divider result in series
    Keyword arguments:
        div -- division ratio
        series -- defined series ('e12' default)
    Return: closes combination in series (R1, R2, error[%])
    '''
    if div==0: raise ValueError('non 0 value expected')
    if series not in SERIES: raise ValueError('unknown series')
    '''r1input = normalize_series(series)*mult'''
    r1input = VALUES[series]
    r2ideal = [enum * div for enum in VALUES[series]]
    r2closes = [get_nearest_in_series(enum) for enum in r2ideal]
    diverrs = [(r2closes[i]/r1input[i])-div for i in range(len(r1input))]
    absdiverrs = [abs(enum)*100 for enum in diverrs]
    mini = absdiverrs.index(min(absdiverrs))
    return [r1input[mini],r2closes[mini],diverrs[mini]*100]
    
''' test '''
print(get_divider(4.56))
