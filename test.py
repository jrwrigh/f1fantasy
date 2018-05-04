import sys
from importlib import reload
import f1classes
import main
reload(f1classes)
reload(main)

global test, test2
if sys.argv[0] == 'race':
    test = f1classes.RaceWeekend()
    test.init_from_ergast()
    test.parse_raceresults()
    if sys.argv[1] == 'pickleboth':
        main.pickle_RaceWeekend(test)
        test2 = main.load_RaceWeekend("data/races/2018_4-Azerbaijan")
elif sys.argv[0] == 'drivertable':
    pass
elif sys.argv[0] == 'reset':
    pass
