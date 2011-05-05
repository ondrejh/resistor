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

MULTMIN = -3
MULTRANGE = 13
MULTIPLIES = [10**(enum+MULTMIN) for enum in range(MULTRANGE)]

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
    multiples = list(MULTIPLIES)
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

def get_divider(div,series='e12',r1series=None,r2series=None,mult=100,esum=None,weight=1):
    ''' Get the best divider result in series
    Keyword arguments:
        div -- division ratio
        series -- defined series ('e12' default) - used when r1/r2 series not defined
        r1series -- defined series for r1 (None default / in this case "series" value used)
        r2series -- defined series for r2 (None default / in this case "series" value used)
        mult -- multiplicator of normalized series (should be 10^n) for r1 selection
        esum -- divider sum wanted result (if not defined - not used)
        weight -- divider value / sum weight [range 1.0 .. 0.0](1..only divider error, 0..only sum error)
    Return: closes combination in series (R1, R2, divider error, sum error)
    '''
    if div==0: raise ValueError('non 0 value expected')
    if series not in SERIES: raise ValueError('unknown series')
    if r1series == None: r1series = series
    if r2series == None: r2series = series
    ## input series
    r1input = [enum * (mult/100) for enum in VALUES[r1series]]
    ## divider
    r2ideal = [enum * div for enum in r1input]
    r2closes = [get_nearest_in_series(enum,r2series) for enum in r2ideal]
    ## divider error
    diverrs = [(r2closes[i]/r1input[i])-div for i in range(len(r1input))]
    absdiverrs = [abs(enum) for enum in diverrs]
    ## divider sum value
    rsum = [r1input[i]+r2closes[i] for i in range(len(r1input))]
    if esum == None: rsumerrs = [0 for i in range(len(r1input))]
    else: rsumerrs = [(rsum[i]-esum)/rsum[i] for i in range(len(r1input))]
    absrsumerrs = [abs(enum) for enum in rsumerrs]
    ## weighted error
    werr = [absdiverrs[i]*weight+absrsumerrs[i]*(1-weight) for i in range(len(r1input))]
    ## the best result index (minimum error)
    mini = werr.index(min(werr))
    ## return (R1,R2,divider error,sum error)
    return [r1input[mini],r2closes[mini],diverrs[mini]*100,rsumerrs[mini]*100]
    
''' test '''
#print('R1: {0[0]:.3f}Ω, R2: {0[1]:.3f}Ω, Divider error: {0[2]:.2f}%, Sum error: {0[3]:.2f}%'.format(get_divider(div=1.586,series='e24',mult=1000,esum=10000,weight=0.8)))
#print('R1: {0[0]:.3f}Ω, R2: {0[1]:.3f}Ω, Divider error: {0[2]:.2f}%, Sum error: {0[3]:.2f}%'.format(get_divider(div=1.586,mult=1000)))
