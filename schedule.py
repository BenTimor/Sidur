import csv
from pathlib import Path

# Preferences:
## 1 - Cant
## 5 - Must
## Anything between, is how much he wants/doesn't want the shift
##
## -1 - Disabled by system
## -2 - Already Embedded

class Employee(dict):
    def __init__(self, name: str, preferences = None):
        if preferences is None:
            preferences = {}

        super().__init__(preferences)
        self.name = name

class Shift:
    def __init__(self, start: int, end: int, employees_needed: int):
        self.start = start
        self.end = end
        self.employees_needed = employees_needed
        self.employees = []

    def clone(self):
        return Shift(self.start, self.end, self.employees_needed)

    def append(self, employee):
        self.employees.append(employee)

    def __len__(self):
        return len(self.employees)

class Day(list):
    def __init__(self, name: str, *shifts: Shift):
        super().__init__([shift.clone() for shift in shifts])
        self.name = name

class Schedule(list):
    def __init__(self, *days: Day):
        super().__init__(days)

    def __str__(self):
        builder = ""
        for day in self:
            builder = f"{builder}{day.name}:\n"
            for shift in day:
                builder = f"{builder}\t{shift.start}-{shift.end}:\n"
                for employee in shift.employees:
                    builder = f"{builder}\t\t{employee.name}\n"
        return builder

    def output_into_file(self, path: str):
        """
        Outputting the schedule into files. Every day gets its own file. path/DAY.csv
        :param path: The path of the FOLDER that the files will be created in
        """
        # Creating path if not exist
        Path(path).mkdir(parents=True, exist_ok=True)
        # Writing every day as a csv file
        for day in self:
            with open(f"{path}/{day.name}.csv", "w") as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # First line / Title
                writer.writerow([" ", day.name])
                for shift in day:
                    employees = ", ".join([e.name for e in shift.employees])
                    writer.writerow([f"{shift.start}-{shift.end}", employees])