import sys
from importlib import reload
import f1classes
import main
reload(f1classes)
reload(main)

if sys.argv[0] == 'race':
    test = f1classes.RaceWeekend()
    test.init_from_ergast()
    test.parse_raceresults()
elif sys.argv[0] == 'drivertable':
    pass
elif sys.argv[0] == 'reset':
    pass
