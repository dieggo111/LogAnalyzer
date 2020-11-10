
import re
import datetime
import time
from datetime import datetime


class LogAnalyzer():
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.main_dict = {}
        self.apply_check_func = []
        self.apply_util_func = []
        self.main_dict["max_lines"] = kwargs.get("max_lines", 500)
        self.output = []

        self.main_dict["exclude"] = kwargs.get("exclude", None)
        if self.main_dict["exclude"]:
            self.apply_check_func.append(self.__check_exclude)

        self.main_dict["include"] = kwargs.get("include", None)
        if self.main_dict["include"]:
            self.apply_check_func.append(self.__check_include)

        self.main_dict["min_date"] = kwargs.get("min_date", None)
        if self.main_dict["min_date"]:
            self.apply_check_func.append(self.__check_min_date)

        self.main_dict["max_date"] = kwargs.get("max_date", None)
        if self.main_dict["max_date"]:
            self.apply_check_func.append(self.__check_max_date)

        self.main_dict["date"] = kwargs.get("date", None)
        if self.main_dict["date"]:
            self.apply_check_func.append(self.__check_date)

        self.main_dict["max_time"] = kwargs.get("max_time", None)
        if self.main_dict["max_time"]:
            self.apply_check_func.append(self.__check_max_time)

        self.main_dict["min_time"] = kwargs.get("min_time", None)
        if self.main_dict["min_time"]:
            self.apply_check_func.append(self.__check_min_time)

        self.main_dict["ignore_line_pattern"] = kwargs.get(
            "ignore_line_pattern", "")
        if self.main_dict["ignore_line_pattern"]:
            self.apply_util_func.append(self.__remove_line_pattern)



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
            line = func(self.main_dict["ignore_line_pattern"], line)
        for func in self.apply_check_func:
            if func(line) is False:
                return False
        return True

    def __remove_line_pattern(self, pattern, line):
        return line.replace(pattern, "")


    def __check_exclude(self, line):
        """Returns True if exclude strings were not found"""

        if self.main_dict["exclude"] is None:
            return True
        for rule in self.main_dict["exclude"]:
            if line.find(rule) != -1:
                return False
        return True


    def __check_include(self, line):
        """Returns True if include strings were found"""

        if self.main_dict["include"] is None:
            return True
        for rule in self.main_dict["include"]:
            if line.find(rule) == -1:
                return False
        return True


    def __check_min_time(self, line):
        line_time = self.__identify_time(line)
        if line_time is None:
            return True
        line_time = datetime.strptime(line_time, "%H:%M:%S")
        if line_time < datetime.strptime(self.main_dict["min_time"], "%H:%M:%S"):
            return False
        return True


    def __check_max_time(self, line):
        line_time = self.__identify_time(line)
        if line_time is None:
            return True
        line_time = datetime.strptime(line_time, "%H:%M:%S")
        if line_time > datetime.strptime(self.main_dict["max_time"], "%H:%M:%S"):
            return False
        return True


    def __check_date(self, line):
        line_date = self.__identify_date(line)
        if line_date is None:
            return True
        line_date = datetime.strptime(line_date, "%d.%m.%Y")
        if line_date != datetime.strptime(self.main_dict["date"], "%d.%m.%Y"):
            return False
        return True

    def __check_min_date(self, line):
        line_date = self.__identify_date(line)
        if line_date is None:
            return True
        line_date = datetime.strptime(line_date, "%d.%m.%Y")
        if line_date > datetime.strptime(self.main_dict["min_date"], "%d.%m.%Y"):
            return False
        return True

    def __check_max_date(self, line):
        line_date = self.__identify_date(line)
        if line_date is None:
            return True
        line_date = datetime.strptime(line_date, "%d.%m.%Y")
        if line_date < datetime.strptime(self.main_dict["max_date"], "%d.%m.%Y"):
            return False
        return True


    def __identify_date(self, line):
        hit = re.search(r"\d{1,2}\.\d{1,2}\.\d{4}", line)
        if hit:
            return hit[0]

    def __identify_time(self, line):
        hit = re.search(r"\d{1,2}:\d{1,2}:\d{1,2}", line)
        if hit:
            return hit[0]




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
