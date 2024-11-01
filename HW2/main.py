import os
import time
from typing import List
from divideandconquer.algorithm import DivideAndConquer
from greedy.algorithm import Greedy
from dynamicprogramming.algorithm import DynamicProgramming
from hybrid.algorithm import HybridAlgorithm
from project import initialize_random_projects, Project
from displayhelper import DisplayHelper
import logging
from matplotlib import pyplot as plt

class Menu:
    def __init__(self):
        """
        Constructor code for initializing the Values for the Menu.
        """        
        self.header = "-"*100
        self.header_text = "\nProject Selection Algorithm\n"
        self.program_menu = """\n1. Divide and Conquer Algorithm\n2. Greedy Algorithm\n3. Dynamic Programming Algorithm with Knapsack Problem\n4. Hybrid Approach\n5. Exit Program\n"""
        self.menu =  self.header + self.header_text + self.header+self.program_menu + self.header
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename='main.log')
        self.logger = logging
        self.total_budget = 100000
        self.dynamic_programming_increment = 5000
        self.display_helper = DisplayHelper()
    
    def initialize_projects(self, n: int) -> List[Project]:
        """Generates a random project based on the value.

        Args:
            n (int): Number of Projects

        Returns:
            List[Project]: List of Projects with Length n
        """
        projects = initialize_random_projects(n)
        return projects
    
    def initialize_project_arrays(self, range_size:range)-> List[List[Project]]:
        """Initialize the Project Arrays based on the range size

        Args:
            range_size (range): Project's Size Range. Say 2^1 to 2^15 or 2^1 to 2^6

        Returns:
            List[List[Project]]: List of Projects with different ranges
        """
        list_projects = list()
        for i in range_size:
            self.logger.info(f"Initializing {2**i} Projects")
            list_projects.append(self.initialize_projects(2**i))
        return list_projects
    
    def display_plot(self, project_size_list: List[int], time_array: List[float], roi_list: List[float], budget: int, algorithm:str):
        """Displays the matplotlib plot to the user.

        Args:
            project_size_list (List[int]): List which provides project's size in each execution of algorithm
            time_array (List[float]): List which provides the time taken for each execution of algorithm
            roi_list (List[float]): List which provides the ROI for each execution of algorithm
            budget (int): Total Budget provided
            algorithm (str): Name of Algorithm which was executed.
        """
        print("Do you need the plot to be displayed? (y/n)")
        choice = input("Enter your choice: ")
        if (choice.lower()=="y"):
            plt.plot(project_size_list, time_array, '--bo')
            plt.title(f"Project Size vs Time for {algorithm} Algorithm with Budget: {budget}")
            plt.xlabel("Project Size")
            plt.ylabel("Time")
            for x_val, y_val in zip(project_size_list, time_array):
                plt.text(x_val, y_val, f"({x_val:.1f}, {y_val:.2f})", fontsize=8, ha='right', color="black")
            plt.show()
            plt.clf()
            plt.close()
            input("Press Enter to continue...")
        elif (choice.lower()=="n"):
            print("Skipping the plot display")
        else:
            print("Skipping the step, as the choice is invalid")
    
    def run_divide_and_conquer(self, algorithm: DivideAndConquer, list_projects: List[List[Project]]):
        """Runs Divide and Conquer Algorithm

        Args:
            algorithm (DivideAndConquer): Divide and Conquer Algorithm Object
            list_projects (List[List[Project]]): List of Projects with different sizes
        """
        logging.info("Running Divide and Conquer Algorithm")
        print("Running Divide and Conquer Algorithm")
        runtime_array = list()
        total_budget = self.total_budget
        projects_selected_array = list()
        projects_size_list = list()
        roi_array = list()
        for i in range(len(list_projects)):
            project_size = len(list_projects[i])
            start_time = time.time()
            selected_projects, roi = algorithm.execute(list_projects[i], total_budget)
            end_time = time.time()
            self.logger.info("Project Size: "+str(project_size))
            self.logger.info("Runtime: "+str(end_time - start_time))
            self.logger.info("ROI: "+str(roi))
            runtime_array.append(end_time - start_time)
            projects_size_list.append(project_size)
            projects_selected_array.append(selected_projects)
            roi_array.append(roi)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_helper.display_time(time_array = runtime_array,
                                             size_array = projects_size_list, 
                                             budget = total_budget,
                                             roi = roi_array, 
                                             project_selected = projects_selected_array)
        self.display_plot(projects_size_list, runtime_array, roi_array, total_budget, algorithm="Divide and Conquer")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')



    def run_greedy(self, algorithm: Greedy, list_projects: List[List[Project]]):
        """Runs the Greedy Algorithm

        Args:
            algorithm (Greedy): Greedy Algorithm Object
            list_projects (List[List[Project]]): List of Projects with different sizes
        """
        print("Running Greedy Algorithm")
        runtime_array = list()
        total_budget = self.total_budget
        projects_selected_array = list()
        projects_size_list = list()
        roi_array = list()
        for i in range(len(list_projects)):
            project_size = len(list_projects[i])
            start_time = time.time()
            selected_projects, roi = algorithm.execute(list_projects[i], total_budget)
            end_time = time.time()
            self.logger.info("Project Size: "+str(project_size))
            self.logger.info("Runtime: "+str(end_time - start_time))
            self.logger.info("ROI: "+str(roi))
            runtime_array.append(end_time - start_time)
            projects_size_list.append(project_size)
            projects_selected_array.append(selected_projects)
            roi_array.append(roi)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_helper.display_time(time_array = runtime_array,
                                             size_array = projects_size_list, 
                                             budget = total_budget,
                                             roi = roi_array, 
                                             project_selected = projects_selected_array)
        self.display_plot(projects_size_list, runtime_array, roi_array, total_budget, algorithm="Greedy")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run_dynamic_programming(self, algorithm: DynamicProgramming, list_projects: List[List[Project]]):
        """Runs the Dynamic Programming Algorithm

        Args:
            algorithm (DynamicProgramming): Dynamic Programming Algorithm Object
            list_projects (List[List[Project]]): List of Projects with different sizes
        """
        print("Running Dynamic Programming Algorithm")
        runtime_array = list()
        total_budget = self.total_budget
        projects_selected_array = list()
        projects_size_list = list()
        roi_array = list()
        for i in range(len(list_projects)):
            project_size = len(list_projects[i])
            start_time = time.time()
            selected_projects, roi = algorithm.execute(list_projects[i])
            end_time = time.time()
            self.logger.info("Project Size: "+str(project_size))
            self.logger.info("Runtime: "+str(end_time - start_time))
            self.logger.info("ROI: "+str(roi))
            runtime_array.append(end_time - start_time)
            projects_size_list.append(project_size)
            projects_selected_array.append(selected_projects)
            roi_array.append(roi)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_helper.display_time(time_array = runtime_array,
                                             size_array = projects_size_list, 
                                             budget = total_budget,
                                             roi = roi_array, 
                                             project_selected = projects_selected_array)
        self.display_plot(projects_size_list, runtime_array, roi_array, total_budget, algorithm="Hybrid")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')

    def run_hybrid(self, algorithm: HybridAlgorithm, list_projects: List[List[Project]]):
        """Runs the Hybrid Algorithm

        Args:
            algorithm (HybridAlgorithm): Hybrid Algorithm Object
            list_projects (List[List[Project]]): List of Projects with different sizes
        """
        print("Running Hybrid Algorithm")
        runtime_array = list()
        total_budget = self.total_budget
        projects_selected_array = list()
        projects_size_list = list()
        roi_array = list()
        for i in range(len(list_projects)):
            project_size = len(list_projects[i])
            start_time = time.time()
            selected_projects, roi = algorithm.execute(list_projects[i])
            end_time = time.time()
            self.logger.info("Project Size: "+str(project_size))
            self.logger.info("Runtime: "+str(end_time - start_time))
            self.logger.info("ROI: "+str(roi))
            runtime_array.append(end_time - start_time)
            projects_size_list.append(project_size)
            projects_selected_array.append(selected_projects)
            roi_array.append(roi)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_helper.display_time(time_array = runtime_array,
                                             size_array = projects_size_list, 
                                             budget = total_budget,
                                             roi = roi_array, 
                                             project_selected = projects_selected_array)
        self.display_plot(projects_size_list, runtime_array, roi_array, total_budget, algorithm="Hybrid Algorithm")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        """
        Run the main menu of the program
        """
        self.logger.info("Main Menu Executed.")
        print("Welcome to the Project Selection Algorithm")
        project_range = range(1,16)
        while(1):
            print(self.menu)
            choice = input("Enter your choice: ")
            self.logger.info(f"User entered choice: {choice}")
            match choice:
                case "1":
                    project_range = range(1,7)
                    divide_and_conquer = DivideAndConquer(logger=None)
                    list_projects = self.initialize_project_arrays(project_range)
                    self.logger.info("Running Divide and Conquer Algorithm")
                    self.run_divide_and_conquer(divide_and_conquer, list_projects)
                case "2":
                    greedy = Greedy(logger=self.logger)
                    list_projects = self.initialize_project_arrays(project_range)
                    self.logger.info("Running Greedy Algorithm")
                    self.run_greedy(greedy, list_projects)
                case "3":
                    dynamic_programming = DynamicProgramming(budget=self.total_budget,increment=self.dynamic_programming_increment,logger=self.logger)
                    list_projects = self.initialize_project_arrays(project_range)
                    self.logger.info("Running Dynamic Programming Algorithm")
                    self.run_dynamic_programming(dynamic_programming, list_projects)
                case "4":
                    hybrid = HybridAlgorithm(budget=self.total_budget,increment=self.dynamic_programming_increment,logger=self.logger)
                    list_projects = self.initialize_project_arrays(project_range)
                    self.logger.info("Running Hybrid Algorithm")
                    self.run_dynamic_programming(hybrid, list_projects)
                case "5":
                    exit()
                case _:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('\033[31m'+"Invalid choice. Please Enter the number between 1 to 5."+'\033[0m')

if __name__ == "__main__":
    menu = Menu()
    menu.run()