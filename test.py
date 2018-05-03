from importlib import reload
import f1classes
reload(f1classes)

test = f1classes.RaceWeekend()
test.init_from_ergast()
test.parse_raceresults()