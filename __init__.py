from .filehandler import *
from .calculations import embedding

def create_schedule(employees_path: str, schedule_path: str, output_folder: str):
    """
    Just running everything in one function, so it'll create a schedule easily
    :param employees_path: The path to the employees file
    :param schedule_path: The path to the schedule file
    :param output_folder: The folder to output into
    """
    # Getting schedule & employees
    schedule = get_schedule(schedule_path)
    employees = get_employees(employees_path, schedule)
    # Embedding the employees into the schedule
    embedding(schedule, employees)
    # Outputting the schedule into files
    schedule.output_into_file(output_folder)