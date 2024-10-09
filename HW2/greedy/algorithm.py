import sys
import os
from typing import List, Tuple
import logging

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(parent)

from project import initialize_projects, Project, initialize_random_projects
from displayhelper import DisplayHelper

class Greedy:
    def seperate_projects(self, projects: List[Project]) -> Tuple[List[Project], List[Project]]:
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
        return whole_projects, fractional_projects

    def select_fractional_projects(self, projects: List[Project],budget: int)-> Tuple[List[Tuple[Project, float]], int, int]:
        """Select the fractional projects on the basis of the roi and budget

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
        return selected_projects, selected_projects_roi, remaining_budget

    def select_whole_projects(self, projects: List[Project], total_roi: int ,budget: int) -> Tuple[List[Tuple[Project, float]], int, int]:
        """Select the whole projects on the basis of the roi and budget

        Args:
            projects (List[Project]): Whole Projects
            budget (int): Total Budget
            total_roi (int): Total ROI

        Returns:
            Tuple[List[Tuple[Project, float]], int, int]: Selected Projects with their fraction, Total ROI and Remaining Budget
        """
        selected_projects = list()
        for project in projects:
            if budget >= project.required_budget:
                budget -= project.required_budget
                total_roi += project.roi
                selected_projects.append((project,1))
        return selected_projects, total_roi, budget
    



    def algorithm(self, projects: List[Project], total_budget: int) -> Tuple[List[Project], int]:
        """Main Algorithm to execute the Greedy Algorithm

        Args:
            projects (List[Project]): Projects 
            total_budget (int): budget to be allocated

        Returns:
            Tuple[List[Project], int]: Selected Projects and the total ROI
        """
        total_roi = 0
        displayhelper = DisplayHelper()  
        # displayhelper.display_projects(projects)      
        whole_projects, fractional_projects = self.seperate_projects(projects)
        fractional_projects.sort(key=lambda project: project.roi/project.required_budget, reverse=True)
        # Fractional Execution
        selected_fractional_projects, fractional_projects_roi, remaining_budget  = self.select_fractional_projects(fractional_projects, total_budget)
        # displayhelper.display_greedy_projects(selected_fractional_projects, fractional_projects_roi)
        whole_projects.sort(key=lambda project: project.roi, reverse=True)
        selected_whole_projects,total_roi, remaining_budget = self.select_whole_projects(whole_projects, fractional_projects_roi, remaining_budget)
        selected_projects = selected_fractional_projects + selected_whole_projects
        # displayhelper.display_greedy_projects(selected_projects, total_roi)
        return selected_projects, total_roi
                # selected_projects = selected_fractional_projects + selected_whole_projects
        # print(fractional_projects_roi, whole_projects_roi)
        # displayhelper = DisplayHelper()
        # displayhelper.display_greedy_projects(selected_projects, total_roi)



# if __name__ == "__main__":
#     projects = initialize_random_projects()
#     total_budget = 100000
#     greedy = Greedy()
#     greedy.algorithm(projects, total_budget)