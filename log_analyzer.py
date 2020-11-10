import re
from log_analyzer_functions import CheckFunctions

class LogAnalyzer():
    def __init__(self, *args, **kwargs):
        self.main_dict = {}
        self.apply_check_func = []
        self.apply_util_func = []
        self.output = []
        self.check_functions = CheckFunctions(self.main_dict)
        self.path = kwargs.get("path")
        self.initialize_functions(**kwargs)
        self.run()

    def initialize_functions(self, **kwargs):
        self.main_dict["max_lines"] = kwargs.get("max_lines", 500)

        self.main_dict["exclude"] = kwargs.get("exclude", None)
        if self.main_dict["exclude"]:
            self.apply_check_func.append(self.check_functions.check_exclude)

        self.main_dict["include"] = kwargs.get("include", None)
        if self.main_dict["include"]:
            self.apply_check_func.append(self.check_functions.check_include)

        self.main_dict["min_date"] = kwargs.get("min_date", None)
        if self.main_dict["min_date"]:
            self.apply_check_func.append(self.check_functions.check_min_date)

        self.main_dict["max_date"] = kwargs.get("max_date", None)
        if self.main_dict["max_date"]:
            self.apply_check_func.append(self.check_functions.check_max_date)

        self.main_dict["date"] = kwargs.get("date", None)
        if self.main_dict["date"]:
            self.apply_check_func.append(self.check_functions.check_date)

        self.main_dict["max_time"] = kwargs.get("max_time", None)
        if self.main_dict["max_time"]:
            self.apply_check_func.append(self.check_functions.check_max_time)

        self.main_dict["min_time"] = kwargs.get("min_time", None)
        if self.main_dict["min_time"]:
            self.apply_check_func.append(self.check_functions.check_min_time)

        self.main_dict["ignore_line_pattern"] = kwargs.get(
            "ignore_line_pattern", [])
        if self.main_dict["ignore_line_pattern"]:
            self.apply_util_func.append(self.ignore_line_pattern)

    def run(self):
        with open(self.path, encoding="utf8") as stream:
            i = 0
            while i < self.main_dict["max_lines"]:
                line = stream.readline()
                line = line.replace("\\n", "")
                if line == "":  # Cuts off if end of file reached
                    break
                if self.__apply_funcs(line) is False:
                    continue
                i += 1
                print(line)
                self.output.append(line)
        stream.close()
        self.__show_analysis(i)


    def __show_analysis(self, counts):
        print(20 * "=")
        print("Found {0} Entries".format(counts))

    def __apply_funcs(self, line):
        for func in self.apply_util_func:
            line = func(line)
        for func in self.apply_check_func:
            if func(line) is False:
                return False
        return True


    def ignore_line_pattern(self, line):
        """Remove certain patterns from a line which are repetative or insignificant"""
        for pattern in self.main_dict["ignore_line_pattern"]:
            line = line.replace(pattern, "")
        return line






if __name__ == "__main__":
    LA=LogAnalyzer(
        "../Logs/PRG/2020-10-09/prg.log",
        # date="10.10.2020",
        min_time="06:36:00",
        # max_time="02:14:00",
        # max_lines=500,
        # exclude=[
        #     "Inside Report Success",
        #     "TempDomain",
        #     "Mindelay cannot be smaller than 1 seconds",
        #     "INSERT",
        #     "[0] => cartavariada"
        # ]
        # ignore_line_pattern=""
    )
    LA.run()
