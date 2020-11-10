from argparse import ArgumentParser
from log_analyzer import LogAnalyzer

PARSER = ArgumentParser()
PARSER.add_argument("path")
PARSER.add_argument("-ml", "--max_lines", default=10)
PARSER.add_argument("-ex", "--exclude", nargs='+', default=None)
PARSER.add_argument("-in", "--include", nargs='+', default=None)
PARSER.add_argument("-nd", "--min_date", default=None)
PARSER.add_argument("-xd", "--max_date", default=None)
PARSER.add_argument("-d", "--date", default=None)
PARSER.add_argument("-xt", "--max_time", default=None)
PARSER.add_argument("-nt", "--min_time", default=None)
PARSER.add_argument("-i", "--ignore_pattern", nargs='+', default=None)
PARSER.add_argument("-a", "--no_analysis", default=None)


KWARGS = vars(PARSER.parse_args())
LOGANALYZER = LogAnalyzer(**KWARGS)
