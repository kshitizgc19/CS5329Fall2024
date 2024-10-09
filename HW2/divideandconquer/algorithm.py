import sys
import os
from typing import List, Tuple
# import logging
import time

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from project import initialize_projects,initialize_random_projects, Project
from displayhelper import DisplayHelper

class DivideAndConquer: 
    def maximize_roi(self, projects: List[Project], total_budget: int) -> Tuple[int, List[Project]]:
        """Maximize the ROI for the given projects and total budget

        Args:
            projects (List[Project]): List of Projects
            total_budget (int): Total Budget of the Project

        Returns:
            Tuple[int, List[Project]]: Selected Projects and the return of investment maximized
        """
        #Base Case Scenario
        project_names = [project.name for project in projects]
        # logging.info(f"Base Case Check for: {project_names} and Total Budget: {total_budget}")
        if total_budget <=0 or not projects:
            # logging.info("Budget Less than 0 or No Projects, returning back to previous call")
            return 0, []       
        selected_project = projects[0]
        remaining_projects = projects[1:]
        included_roi = 0
        remaining_budget = total_budget - selected_project.required_budget
        required_budget = selected_project.required_budget
        roi = selected_project.roi
        project_type = selected_project.project_type
        included_project = list()
        max_included_roi = 0
        max_excluded_roi = 0
        excluded_projects = list()
        # logging.info(f"Selecting project: {selected_project.name} with ROI: {roi} and Budget: {required_budget}")
        excluded_projects = [project.name for project in remaining_projects]
        # logging.info(f"Excluded Projects: {excluded_projects}")
        # logging.info("Maximum ROI Calculation for excluded projects, recursion call")
        # Case 1: Getting the roi for the excluded/remaining projects
        max_excluded_roi, projects_excluded = self.maximize_roi(remaining_projects, total_budget)
        excluded_projects = [project.name for project in projects_excluded]
        # logging.info(f"Max Excluded ROI: {max_excluded_roi} for Projects: {excluded_projects}")
        # Case 2: Getting the roi for the included project
        # logging.info("Maximum ROI Calculation for included projects, recursion call")
        if project_type.lower() == "whole" and total_budget >= required_budget:
            # logging.info(f"Project Name: {selected_project.name}, Project Type: Whole, ")
            included_roi, project_included = self.maximize_roi(remaining_projects, remaining_budget) 
            max_included_roi = roi + included_roi
            included_project = [selected_project] + project_included
            included_project_names = [project.name for project in included_project]
            # logging.info(f"Max Included ROI: {max_included_roi} for Projects: {included_project_names}")
        elif project_type.lower() == "fractional":
            if total_budget >= required_budget:
                # logging.info(f"Fractional Project, name: {selected_project.name}, Selecting as whole, total budget > required budget")
                included_roi, project_included = self.maximize_roi(remaining_projects, remaining_budget)
                max_included_roi = roi + included_roi
                included_project = [selected_project] + project_included
                included_project_names = [project.name for project in included_project]
                # logging.info(f"Max Included ROI: {max_included_roi} for Projects: {included_project_names}")
            else:
                # logging.info(f"Fractional Project, name: {selected_project.name}, Selecting as fractional, total budget < required budget")
                fractional_roi = (total_budget/required_budget) * roi
                included_roi, project_included = self.maximize_roi(remaining_projects, 0)
                max_included_roi = fractional_roi + included_roi
                included_project = [selected_project] + project_included
                included_project_names = [project.name for project in included_project]
                # logging.info(f"Max Included ROI: {max_included_roi} for Projects: {included_project_names}")
        if max_included_roi > max_excluded_roi:
            return max_included_roi, included_project
        else:
            return max_excluded_roi, projects_excluded

    def algorithm(self, projects: List[Project], total_budget: int) -> Tuple[List[Project], int]:
        """Main Algorithm to execute the Divide and Conquer Algorithm

        Args:
            projects (List[Project]): Projects to be selected
            total_budget (int): Total Budget of the Project

        Returns:
            Tuple[List[Project], int]: Selected Projects and the total ROI
        """
        roi, projects_selected = self.maximize_roi(projects, total_budget)
        display_helper = DisplayHelper()
        return projects_selected, roi
        # display_helper.display_projects(projects)
        # display_helper.display_projects(projects_selected)