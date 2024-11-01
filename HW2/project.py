import random
from typing import List

class Project:
    def __init__(self,name: str,project_type: str,required_budget: float, roi: float):
        """Project class to store the project details

        Args:
            name (str): Name of the Project
            project_type (str): Fractional and Whole Project
            required_budget (float): Budget of the project
            roi (float): Return on Investment
        """
        self.name = name
        self.project_type = project_type
        self.required_budget = required_budget
        self.roi = roi

def initialize_projects() -> List[Project]:
    """Generates the projects for the program
        For Testing Purpose Only

    Returns:
        List[Project]: Projects Array that are created.
    """
    project_values = [
        ["P1", "Fractional", 30000, 90000],
        ["P2", "Whole", 20000, 50000],
        ['P3', "Fractional", 10000, 30000],
        ["P4", "Whole", 25000, 60000],
        ["P5", "Whole", 15000, 35000],
    ]
    projects = list()
    for value in project_values:
        projects.append(Project(value[0], value[1], value[2], value[3]))
    return projects

def initialize_random_projects(num_projects : int = 10) -> List[Project]:
    """Generates Random Projects for the program

    Args:
        num_projects (int, optional): Number of Projects to be generated randomly. Defaults to 10.

    Returns:
        List[Project]:Projects Array that are created.
    """
    projects = list()
    for i in range(num_projects):
        name = "P" + str(i+1)
        project_type = random.choice(["Whole", "Fractional"])
        budget = random.randint(1,10)*5000
        roi = budget * random.randint(1,5)
        projects.append(Project(name=name, project_type=project_type, required_budget=budget, roi=roi))
    return projects
    