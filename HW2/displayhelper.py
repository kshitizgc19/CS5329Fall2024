from typing import List, Tuple
from project import Project

class DisplayHelper:
    def display_time(self, time_array: List[int], size_array:List[int], budget:int, roi:int, project_selected: List[Project]):
        """Display the time taken for the execution of the algorithm in the form of a table

        Args:
            time_array (List[int]): Execution time for each project size
            size_array (List[int]): Size of the projects
            budget (int): Total budget of the projects
            roi (int): Return on Investment for each project size
            project_selected (List[Project]): Selected projects for each project size
        """
        print('-'*100)
        print("SN\tProject Size\tTotal Budget\tTotal ROI\tTime Executed")
        print('-'*100)
        for i in range(len(time_array)):
            print(f"{i+1}\t{size_array[i]}\t\t{budget}\t\t{int(roi[i])}\t\t{round(time_array[i], 5)}")
        print('-'*100)

    def display_projects(self, projects: List[Project]) :
        """Display the projects in the form of a table

        Args:
            projects (List[Project]): Selected projects
        """
        print('-'*100)
        print("SN\tProject Name\tProject Type\tBudget\tROI")
        print('-'*100)
        for i in range(len(projects)):
            if projects[i].project_type.lower() == "whole":
                print(f"{i}\t{projects[i].name}\t\t{projects[i].project_type}\t\t{projects[i].required_budget}\t{projects[i].roi}")
            else:
                print(f"{i}\t{projects[i].name}\t\t{projects[i].project_type}\t{projects[i].required_budget}\t{projects[i].roi}")
            print('-'*100)

    def display_greedy_projects(self, projects:List[Tuple[Project,float]], total_roi: float) -> None:
        """Display the selected projects and the total ROI done with the greedy algorithm

        Args:
            projects (List[Tuple[Project,float]]): Projects with their fractional size
            total_roi (float): Total Roi of the project
        """
        print('-'*100)
        print("SN\tProject Name\tProject Type\tBudget\tROI\tFraction")
        print('-'*100)
        for i, (project, fraction) in enumerate(projects):
            if project.project_type.lower() == "whole":
                print(f"{i}\t{project.name}\t\t{project.project_type}\t\t{project.required_budget}\t{project.roi}\t{fraction}")
            else:
                print(f"{i}\t{project.name}\t\t{project.project_type}\t{project.required_budget}\t{project.roi}\t{fraction}")
            print('-'*100)
        print(f"Total ROI: {total_roi}")
        print('-'*100)
    
    def display_knapsack_table(self, roi, selected_projects, whole_projects, increment) -> None:
        print("\n")
        print("Dynamic Programming Table of ROI for Whole Projects")
        print('-'*120)
        for i in range(len(roi[0])):
            if i == 0:
                print("Projects\\Budget \t", i*increment, end="\t")
            else:
                print(i*increment, end="\t")
        print()
        print('-'*120)
        projects_list = list()
        tab_len = len(roi)
        for i in range(len(roi)):
            if i == 0:
                pass
            else:
                projects_list.append(whole_projects[i-1].name)
                tab_len-=1
            if i == 0:
                print(projects_list, end="\t"*(tab_len-1))
            else:
                print(projects_list, end="\t"*tab_len)
            for j in range(len(roi[0])):
                print(roi[i][j], end="\t")
            print()
        print('-'*120)
        print("Selected Projects:", end="\t")
        for project in selected_projects[-1][-1]:
            print(project.name, end="\t")