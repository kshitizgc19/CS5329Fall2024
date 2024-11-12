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

class DynamicProgramming:
    def __init__(self, budget: int, increment: int, logger: logging = None):
        """Constructor code for Dynamic Programming Algorithm

        Args:
            budget (int): total budget
            increment (int): divider value for the dynamic programming table
            logger (logging, optional): Logger for logging out the execution. Defaults to None.
        """
        self.budget = budget
        self.increment = increment
        self.partition_size = floor_division(budget, increment)+1
        self.logger = logger

    def seperate_projects(self, projects: List[Project])-> Tuple[List[Project], List[Project]]:
        """Seperate the projects into whole and fractional projects

        Args:
            projects (List[Project]): Projects that are to be divided

        Returns:
            Tuple[List[Project], List[Project]]: Divided lists of whole and fractional projects
        """
        whole_projects = list()
        fractional_projects = list()
        for project in projects:
            if project.project_type.lower() == "whole":
                whole_projects.append(project)
            elif project.project_type.lower() == "fractional":
                fractional_projects.append(project)
        self.logger.info(f"Whole Projects: {len(whole_projects)} and Fractional Projects: {len(fractional_projects)}")
        return whole_projects, fractional_projects

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
        #0(n)
        for i in range(n+1):
            row = [0] * self.partition_size 
            array.append(row)
        self.logger.info(f"Initialized Dynamic Programming Table with {n} Rows and {self.partition_size} Columns with all zeros")
        #O(n*partition_size)
        for _ in range(n+1):
            project_row = list()
            for _ in range(self.partition_size):
                project_row.append([])
            selected_projects.append(project_row)
        self.logger.info(f"Initialized Dynamic Programming Table with {n} Rows and {self.partition_size} Columns with all lists `[]`")
        return array, selected_projects
    
    def fractional_project_selection(self, projects: List[Project], budget: int)-> Tuple[int, List[Tuple[Project, float]], int]:
        """Select the fractional projects based on the ROI and Budget

        Args:
            projects (List[Project]): List of Projects
            budget (int): Total Budget

        Returns:
            Tuple[int, List[Tuple[Project, float]], int]: Total ROI, Selected Projects with their fraction and Remaining Budget
        """
        projects.sort(key=lambda x: x.roi/x.required_budget, reverse=True)
        total_roi = 0
        selected_projects = list()
        for project in projects:
            if project.required_budget <= budget:
                total_roi += project.roi
                budget -= project.required_budget
                selected_projects.append((project, 1))
            else:
                total_roi += project.roi * (budget/project.required_budget)
                budget = 0
                selected_projects.append((project, budget/project.required_budget))
                break
        return total_roi, selected_projects, budget
    
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
        #O(n*partition_size)
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
        self.logger.info(f"Selected Whole Projects: {len(selected_projects[-1][-1])} with ROI: {dp_table[-1][-1]}")
        return dp_table, selected_projects
    
    def calculate_remaining_budget(self, selected_projects:List[Project])->int:
        """Calculates the remaining budget after selecting the projects

        Args:
            selected_projects (List[Project]): Selected Projects

        Returns:
            int: Remaining Budget
        """
        total_budget = self.budget
        budgets_used = 0
        for project in selected_projects:
            budgets_used += project.required_budget
        return total_budget - budgets_used

    def execute(self, projects: List[Project])-> Tuple[List[Project], int]:
        """Used to execute the Dynamic Programming Algorithm

        Args:
            projects (List[Project]): List of Projects to be selected from Algorithm

        Returns:
            Tuple[List[Project], int]: Selected Projects and Total ROI
        """
        increment = self.increment
        budget = self.budget
        whole_projects, fractional_projects = self.seperate_projects(projects)
        self.logger.info("Selecting Whole Projects")
        dp_table, selected_whole_projects  = self.whole_project_selection(whole_projects)
        remaining_budget = self.calculate_remaining_budget(selected_whole_projects[-1][-1])
        self.logger.info(f"Selecting Fractional Projects for the remaining budget of {remaining_budget}")
        roi_fractional, selected_fractional_projects, remaining_budget = self.fractional_project_selection(fractional_projects, remaining_budget)
        total_roi = dp_table[-1][-1] + roi_fractional
        selected_projects = selected_whole_projects[-1][-1] + selected_fractional_projects
        self.logger.info(f"Total ROI: {total_roi} with Selected Projects: {len(selected_projects)}")
        return selected_projects, total_roi

# if __name__ == "__main__":
#     projects = initialize_random_projects(num_projects=5)
#     total_budget = 100000
#     increment = 5000
#     helper = DisplayHelper()
#     helper.display_projects(projects)
#     knapsack = DynamicProgramming(budget=total_budget, increment=increment)
#     knapsack.execute(projects)