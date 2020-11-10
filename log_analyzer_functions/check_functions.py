from datetime import datetime
import re

class CheckFunctions():

    def __init__(self, main_dict):
        self.main_dict = main_dict

    def check_exclude(self, line):
        """Returns True if exclude strings were not found"""

        if self.main_dict["exclude"] is None:
            return True
        for rule in self.main_dict["exclude"]:
            if line.find(rule) != -1:
                return False
        return True


    def check_include(self, line):
        """Returns True if include strings were found"""

        if self.main_dict["include"] is None:
            return True
        for rule in self.main_dict["include"]:
            if line.find(rule) == -1:
                return False
        return True


    def check_min_time(self, line):
        line_time = self.__identify_time(line)
        if line_time is None:
            return True
        line_time = datetime.strptime(line_time, "%H:%M:%S")
        if line_time < datetime.strptime(self.main_dict["min_time"], "%H:%M:%S"):
            return False
        return True


    def check_max_time(self, line):
        line_time = self.__identify_time(line)
        if line_time is None:
            return True
        line_time = datetime.strptime(line_time, "%H:%M:%S")
        if line_time > datetime.strptime(self.main_dict["max_time"], "%H:%M:%S"):
            return False
        return True

    def check_date(self, line):
        line_date = self.__identify_date(line)
        if line_date is None:
            return True
        line_date = datetime.strptime(line_date, "%d.%m.%Y")
        if line_date != datetime.strptime(self.main_dict["date"], "%d.%m.%Y"):
            return False
        return True

    def check_min_date(self, line):
        line_date = self.__identify_date(line)
        if line_date is None:
            return True
        line_date = datetime.strptime(line_date, "%d.%m.%Y")
        if line_date > datetime.strptime(self.main_dict["min_date"], "%d.%m.%Y"):
            return False
        return True

    def check_max_date(self, line):
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