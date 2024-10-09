import os
import time
from divideandconquer.algorithm import DivideAndConquer
from greedy.algorithm import Greedy
from project import initialize_random_projects, Project
from displayhelper import DisplayHelper

class Menu:
    def __init__(self):
        self.header = "-"*100
        self.header_text = "\nProject Selection Algorithm\n"
        self.program_menu = """\n1. Divide and Conquer Algorithm\n2. Greedy Algorithm\n3. Dynamic Programming Algorithm with Knapsack Problem\n4. Hybrid Approach\n5. Exit Program\n"""
        self.menu =  self.header + self.header_text + self.header+self.program_menu + self.header
        self.project_size = range(1,16)
        self.total_budget = 100000
        self.time_array = list()
        self.display_helper = DisplayHelper()
    
    def execute_divide_and_conquer_algorithm(self, algorithm_function):
        """Execute the divide and conquer algorithm and displays the time taken for the execution

        Args:
            algorithm_function (func): Instance of the function to be executed.
        """
        self.time_array.clear()
        self.project_size = range(1,8)
        selected_projects = list()
        project_size_list = list()
        roi_list = list()
        for i in self.project_size:
            project_size = (2)**i
            project_size_list.append(project_size)
            projects = initialize_random_projects(num_projects=project_size)
            start_time = time.time()
            projects_selected, total_roi = algorithm_function(projects, self.total_budget)
            roi_list.append(total_roi)
            selected_projects.append(projects_selected)
            end_time = time.time()
            self.time_array.append(end_time-start_time)
            if self.display_table:
                self.display_helper.display_projects(projects)
        self.display_helper.display_time(self.time_array, project_size_list, self.total_budget, roi_list, selected_projects)
        input("Press Enter to continue")
        # self.display_helper.display_time(self.time_array)
    
    def execute_greedy_algorithm(self, algorithm_function):
        """Execute the Greedy and displays the time taken for the execution

        Args:
            algorithm_function (func): Instance of the function to be executed.
        """
        self.time_array.clear()
        selected_projects = list()
        project_size_list = list()
        roi_list = list()
        list_projects = list()
        for i in self.project_size:
            projects_list = list()
            project_size = (2)**i
            project_size_list.append(project_size)
            projects = initialize_random_projects(num_projects=project_size)
            start_time = time.time()
            projects_selected, total_roi = algorithm_function(projects, self.total_budget)
            for i in range(len(projects_selected)):
                projects_list.append(projects_selected[i][0])
            roi_list.append(total_roi)
            selected_projects.append(projects_selected)
            end_time = time.time()
            self.time_array.append(end_time-start_time)
            list_projects.append(projects_list)
            if self.display_table:
                self.display_helper.display_projects(projects)
        self.display_helper.display_time(self.time_array, project_size_list, self.total_budget, roi_list, selected_projects)
        input("Press Enter to continue")
        

    def run(self):
        """
        Run the main menu of the program
        """
        print("Welcome to the Project Selection Algorithm")
        print("Do you want to display the table for the projects?")
        choice = input("Enter Y for Yes and N for No: ")
        if choice.lower() == "y":
            self.display_table = True
        elif choice.lower() == "n":
            self.display_table = False
        while(1):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.menu)
            choice = int(input("Enter your choice: "))
            match choice:
                case 1:
                    divide_and_conquer = DivideAndConquer()
                    self.execute_divide_and_conquer_algorithm(divide_and_conquer.algorithm)
                case 2:
                    greedy = Greedy()
                    self.execute_greedy_algorithm(greedy.algorithm)
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    exit()

if __name__ == "__main__":
    menu = Menu()
    menu.run()