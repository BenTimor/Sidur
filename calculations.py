from typing import List
from .schedule import *
from random import shuffle
from . import config

def embedding(schedule: Schedule, employees: List[Employee]):
    """
    Embedding all of the employees into the schedule
    :param schedule: The schedule
    :param employees: The employees
    """
    # Embedding the priorities from 5 to 2
    for priority in range(5, 1, -1):
        for day_number in range(len(schedule)):
            day = schedule[day_number]
            for shift in day:
                # In the first run of every shift, set all the empty shifts of the employees to 3
                if priority == 5:
                    set_shift_employees(shift, employees)

                # Get & Shuffle employees with this priority
                available_employees = priority_employees(shift, employees, priority)
                shuffle(available_employees)

                # If the priority is 5 we must embed the employees
                if priority == 5:
                    for employee in available_employees:
                        embed_employee(shift, schedule, employee)
                    continue

                # Check how many employees needed, if there are not needed, continue
                employees_needed = shift.employees_needed - len(shift.employees)

                while available_employees:
                    # If needed, add the employees
                    least_working = least_working_employees(available_employees)

                    # If we don't need any more employees, break
                    if employees_needed <= 0:
                        break

                    # If we have more than enough employees, add just the right amount
                    if len(least_working) >= employees_needed:
                        for employee in least_working[:employees_needed]:
                            embed_employee(shift, schedule, employee)
                            available_employees.remove(employee)
                            employees_needed -= 1

                    # If we don't have enough employees (in this run!), add all of them
                    else:
                        for employee in least_working:
                            embed_employee(shift, schedule, employee)
                            available_employees.remove(employee)
                            employees_needed -= 1

                else:
                    # Check if we have enough employees
                    if priority == 2 and employees_needed > 0:
                        print(f"Not enough employees for day {day_number} / shift {shift.start}-{shift.end}")

def embed_employee(shift: Shift, schedule: Schedule, employee: Employee, past_check=False):
    """
    Adding an employee into a shift
    :param shift: The shift
    :param schedule: All of the schedule
    :param employee: The employee
    :param past_check: If it's true, the function won't add the employee to any shift, it'll just set the past shifts in config.hours range to -1.
    """
    if not past_check:
        shift.append(employee)
        # Setting the shift to -2 so he won't be embedded again
        employee[shift] = -2

    allowed = False
    add = 0

    past_check = -1 if past_check else 1 # Past check just blocking past shifts via config time, so he won't be working in config.time hours before shift

    for day in schedule[::past_check]:
        if allowed:
            add += 24
        same_day = False
        for day_shift in day[::past_check]:
            # Since the moment we pass on his shift, we'll check the rest of the shifts
            if day_shift == shift:
                allowed = True
                same_day = True
                continue

            # If needed, disabling all shifts in the same day
            if same_day and config.one_shift_per_day:
                employee[day_shift] = -1
                continue

            if allowed:
                # If the shift starts in less than X hours (from the config) he won't be able to be embedded into it
                if shift.end < shift.start: # If the shift ends before it's started (for example, 18-02), we have to add 24 hours to the end because it the day after
                    if day_shift.start + add > shift.end + 24 + config.time_between_shifts:
                        return
                    else:
                        employee[day_shift] = -1
                else:
                    if day_shift.start+add > shift.end+config.time_between_shifts:
                        return
                    else:
                        employee[day_shift] = -1

    if not past_check:
        embed_employee(shift, schedule, employee, True)

# You can't have shift with not priority. So we'll set every shift to 3.
def set_shift_employees(shift, employees: List[Employee]):
    """
    Setting the priority of the shift to 3 if it doesn't have any priority
    :param shift: The shift
    :param employees: List of employees to set it on
    """
    for employee in employees:
        if shift not in employee:
            employee[shift] = 3

def priority_employees(shift: Shift, employees: List[Employee], priority: int) -> List[Employee]:
    """
    :param shift: What shift you want the employees to work at
    :param employees: List of all of the employees you want to check
    :param priority: What is the priority
    :return: List of all of the employees which has this priority for the shift
    """
    return [employee for employee in employees if employee[shift] == priority]

def least_working_employees(employees: List[Employee]) -> List[Employee]:
    """
    :param employees: List of the employees to check
    :return: The employees which work the least
    """
    if not employees:
        return []

    available_employees = []
    least = shifts_amount(employees[0])

    for employee in employees:
        shifts = shifts_amount(employee)

        if shifts == least:
            available_employees.append(employee)

        if shifts < least:
            least = shifts
            available_employees = [employee]

    return available_employees

def shifts_amount(employee: Employee) -> int:
    """
    :param employee: The employee to check
    :return: The amount of shifts that the employee has
    """
    return len([v for v in employee.values() if v == -2])