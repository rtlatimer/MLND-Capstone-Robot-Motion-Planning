# Robot Motion Planning
## Plot and Navigate a Virtual Maze

### Capstone Project for Udacity's Machine Learning Engineer Nanodegree
by Robert Latimer

#### Description

The goal of this project is to program a robotic mouse to simulate a [Micromouse competition](https://en.wikipedia.org/wiki/Micromouse) in a virtual maze environment. The robot will first explore and chart an unfamiliar maze, identify an optimal path to the designated goal area, then travel the identified optimal path to the goal. Using an A* algorithm and a Dynamic Programming approach, I was able to develop a model where the robot reads and translates information from its sensors, creates a virtual map of each maze it explores, identifies an optimal path to the goal, and then accurately travels the path to the goal - all while outperforming a defined benchmark model. 

For full detail of the project, please see 'capstone_report.pdf'. All programmed robot logic can be found in 'robot.py'.

### To Run the Code:

#### Install

* Python 2.7
* [NumPy](http://www.numpy.org/)

#### Code

* robot.py - This establishes the Robot class, but is the main script where modifications were made to the project.
* tester.py - This script is run to test the robot’s ability to navigate the mazes.
* maze.py - This script is used to construct each maze and interacts with the robot whenever it is moving or checking its sensors.
* showmaze.py - This script creates a visual layout of each maze.
* globalvariables.py - This script stores all of the global dictionaries used in the project.
test_maze_##.txt - These consist of three sample mazes to test the robot.

#### Supplementary Files

* test_maze_01.txt - This file contains the information for Test Maze 1. Dimensions: 12-by-12
* test_maze_02.txt - This file contains the information for Test Maze 2. Dimensions: 14-by-14
* test_maze_03.txt - This file contains the information for Test Maze 3. Dimensions: 16-by-16
* capstone_report.pdf - This report summarizes the development process of this project and provides detailed explanations and visuals to aid in understanding.

#### To Display a Visual Representation of Maze

In terminal or command window, enter and run the following:
Test Maze 1 - `$ python showmaze.py test_maze_01.txt`
Test Maze 2 - `$ python showmaze.py test_maze_02.txt`
Test Maze 3 - `$ python showmaze.py test_maze_03.txt`

#### To Test the Robot in a Maze

In terminal or command window, enter and run the following:
Test Maze 1 - `$ python tester.py test_maze_01.txt`
Test Maze 2 - `$ python tester.py test_maze_02.txt`
Test Maze 3 - `$ python tester.py test_maze_03.txt`