from typing import List
from .schedule import *
import csv
import json

def get_schedule(path: str) -> Schedule:
    """
    Reading the file and converting it into a Schedule object
    :param path: The path of the file
    :return: Schedule object
    """
    days = []
    days_dict = {}

    # Reading the shifts and putting it in dict like {Day1: [Shift1, Shift2], Day2: [....]...}
    with open(path, "r") as file:
        for row in csv.DictReader(file):
            for day, shift in row.items():
                if day not in days_dict:
                    days_dict[day] = []

                days_dict[day].append(shift)

    # Converting the days_dict to list of Day objects.
    for day, shifts in days_dict.items():
        shift_list = []
        for shift in shifts:
            start, end = shift.split("-") # The shifts structure is START-END:EMPLOYEES_NEEDED
            end, employees_needed = end.split(":")
            shift_list.append(Shift(int(start), int(end), int(employees_needed)))

        days.append(Day(day, *shift_list))

    return Schedule(*days)

def get_employees(path: str, schedule: Schedule) -> List[Employee]:
    """
    Reading file and returning a list of all of the employees
    :param path: The path of the file
    :param schedule: The schedule object (used for preferences*)
    :return: List of employees
    """
    employees = []

    with open(path, "r") as file:
        for name, preferences in json.load(file).items():
            new_preferences = {}
            if not preferences:
                employees.append(Employee(name))
                continue

            # Creating a dictionary which contains DayName:DayObject, so we'll be able to get the days easily
            days_dict = {}
            for day in schedule:
                days_dict[day.name] = day

            # Getting the days, shifts and priorities from the json file per every employee
            for day, shift_priority in preferences.items():
                for shift, priority in shift_priority.items():
                    # Getting all of the shifts from the day which we want to add a priority to
                    # Checking if the shift is what we're looking for, if it is we're putting it into the prefernces
                    day_shift = [s for s in days_dict[day] if f"{s.start}-{s.end}" == shift][0]
                    new_preferences[day_shift] = priority

            # Finally, adding the employee object
            employees.append(Employee(name, new_preferences))

    return employees