import sys
import os
from typing import List, Tuple
import logging
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from project import  Project

def floor_division(a: int, b: int)-> int:
    """Floor Division of two numbers

    Args:
        a (int): Dividend
        b (int): Divisor

    Returns:
        int: Quotient
    """
    return a//b

class HybridAlgorithm:
    def __init__(self, budget: int, increment: int, logger: logging = None):
        """Constructor code for Hybrid Algorithm

        Args:
            budget (int): total budget
            increment (int): divider value for the dynamic programming table
            logger (logging, optional): Logger for logging out the execution. Defaults to None.
        """
        self.budget = budget
        self.increment = increment
        self.partition_size = floor_division(budget, increment)+1
        self.logger = logger

    def split_projects(self, projects: List[Project])-> Tuple[List[Project], List[Project]]:
        """Split the projects into whole and fractional projects using divide and conquer approach

        Args:
            projects (List[Project]): List of projects to be divided

        Returns:
            Tuple[List[Project], List[Project]]: Whole and Fractional Projects as tuple
        """
        if len(projects) == 0:
            return list(), list()
        if len(projects) == 1:
            if projects[0].project_type.lower() == "fractional":
                return list(projects), list()
            else:
                return list(), list(projects)
        mid = floor_division(len(projects),2)
        left = projects[:mid]
        right = projects[mid:]
        fractional_left, whole_left = self.split_projects(left)
        fractional_right, whole_right = self.split_projects(right)
        return fractional_left+fractional_right, whole_left+whole_right
    
    def select_fractional_projects(self, projects: List[Project],budget: int)-> Tuple[List[Tuple[Project, float]], int, int]:
        """Select the fractional projects on the basis of the roi and budget with greedy approach

        Args:
            projects (List[Project]): Fractional Projects
            budget (int): Total Budget

        Returns:
            Tuple[List[Tuple[Project, float]], int, int]: Selected Projects with their fraction, Total ROI and Remaining Budget
        """
        selected_projects = list()
        allocated_budget = 0
        selected_projects_roi = 0
        remaining_budget = 0
        for project in projects:
            if allocated_budget + project.required_budget <= budget:
                selected_projects.append((project,1))
                allocated_budget += project.required_budget
                selected_projects_roi += project.roi
                remaining_budget = budget - allocated_budget
            else:
                remaining_budget = budget - allocated_budget
                can_complete_work = remaining_budget/project.required_budget
                fractional_roi = can_complete_work * project.roi
                selected_projects_roi += fractional_roi
                selected_projects.append((project, can_complete_work))
                break
        self.logger.info(f"Selected Fractional Projects: {len(selected_projects)} with ROI: {selected_projects_roi} and Remaining Budget: {remaining_budget}")
        return selected_projects, selected_projects_roi, remaining_budget
    
    def initialize_arrays(self, n:int)-> Tuple[List[List[int]],List[List[List[Project]]]]:
        """Initialize the Dynamic Programming Table with all zeros and selected project table for each cell with empty list.
        Divides the table into n rows and partition_size columns
        Partition Size is calculated by dividing the total budget with the increment value and adding 1 to it.

        Args:
            n (int): Number of Projects

        Returns:
            Tuple[List[List[int]],List[List[List[Project]]]]: Both Dynamic Programming Table and Selected Projects Table
        """
        array = list()
        selected_projects = list()
        for i in range(n+1):
            row = [0] * self.partition_size 
            array.append(row)
        self.logger.info(f"Initialized Dynamic Programming Table with {n} Rows and {self.partition_size} Columns with all zeros")
        for _ in range(n+1):
            project_row = list()
            for _ in range(self.partition_size):
                project_row.append([])
            selected_projects.append(project_row)
        self.logger.info(f"Initialized Dynamic Programming Table with {n} Rows and {self.partition_size} Columns with all lists `[]`")
        return array, selected_projects

    def whole_project_selection(self, projects:List[Project])->Tuple[List[List[int]],List[List[List[Project]]]]:
        """Select the whole projects based on the ROI and Budget using Dynamic Programming Algorithm

        Args:
            projects (List[Project]): List of Projects

        Returns:
            Tuple[List[List[int]],List[List[List[Project]]]]: Dynamic Programming Table with ROI And Selected Projects table with Selected Projects
        """
        increment = self.increment
        num_projects = len(projects)
        dp_table, selected_projects = self.initialize_arrays(num_projects)
        for i in range(1, num_projects+1):
            for j in range(self.partition_size):
                budget_slab = j*increment
                if projects[i-1].required_budget <= budget_slab:
                    index  = floor_division(projects[i-1].required_budget, increment)
                    if dp_table[i-1][j] < dp_table[i-1][j-index] + projects[i-1].roi:
                        dp_table[i][j] = dp_table[i-1][j-index] + projects[i-1].roi
                        selected_projects[i][j] = selected_projects[i-1][j-index] + [projects[i-1]]
                    else:
                        dp_table[i][j] = dp_table[i-1][j]
                        selected_projects[i][j] = selected_projects[i-1][j]
                else:
                    dp_table[i][j] = dp_table[i-1][j]
                    selected_projects[i][j] = selected_projects[i-1][j]
        return dp_table, selected_projects

    def execute(self, projects: List[Project]) -> Tuple[List[Project], int]:
        """Main Algorithm to execute the Greedy Algorithm

        Args:
            projects (List[Project]): Projects to be selected

        Returns:
            Tuple[List[Project], int]: Selected Projects and the total ROI
        """
        total_budget = self.budget
        total_roi = 0
        fractional_projects, whole_projects = self.split_projects(projects)
        self.logger.info(f"Whole Projects: {len(whole_projects)} and Fractional Projects: {len(fractional_projects)}")
        self.logger.info("Sorting Fractional Projects on the basis of ROI")
        fractional_projects.sort(key=lambda project: project.roi/project.required_budget, reverse=True)
        selected_fractional_projects, selected_projects_roi, remaining_budget = self.select_fractional_projects(fractional_projects, total_budget)
        total_roi += selected_projects_roi
        self.logger.info("Selecting Whole Projects using Dynamic Programming Algorithm")
        dp_table, selected_projects_table = self.whole_project_selection(whole_projects)
        index = floor_division(remaining_budget, self.increment)
        selected_whole_projects = selected_projects_table[-1][index]
        self.logger.info(f"Selected Whole Projects: {len(selected_projects_table[-1][index])} with ROI: {dp_table[-1][index]}")
        total_roi += dp_table[-1][index]
        selected_projects = selected_fractional_projects + selected_whole_projects
        self.logger.info(f"Total Selected Projects: {len(selected_projects)} with Total ROI: {total_roi}")
        return selected_projects, total_roi



        


        
# if __name__ == '__main__':
#     hybrid = HybridAlgorithm()
#     hybrid.execute_algorithm()