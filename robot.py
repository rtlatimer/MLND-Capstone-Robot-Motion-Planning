import numpy as np
from globalvariables import *

# python tester.py test_maze_01.txt
# python tester.py test_maze_02.txt
# python tester.py test_maze_03.txt

class Robot(object):
    def __init__(self, maze_dim):
        
        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.maze_area = maze_dim ** 2.
        self.maze_grid = np.zeros((maze_dim, maze_dim), dtype=np.int) # Grid for wall locations for each maze.
        self.discovered_goal = False
        self.path_grid = np.zeros((maze_dim, maze_dim), dtype=np.int) # Grid for path
        self.path_value = [[99 for row in range(maze_dim)] for col in range(maze_dim)] # Value score starting from goal and working way back.
        self.policy_grid = [[' ' for row in range(maze_dim)] for col in range(maze_dim)] # Grid to map optimal route.
        self.found_goal = [maze_dim/2 - 1, maze_dim/2] or [maze_dim/2, maze_dim/2] or [maze_dim/2, maze_dim/2 - 1] or [maze_dim/2 - 1, maze_dim/2 - 1]  # Goal area in maze center
        self.heuristic = [[min(abs(row-maze_dim/2+1), abs(row-maze_dim/2))+min(abs(col-maze_dim/2+1), abs(col-maze_dim/2)) for row in range(maze_dim)] for col in range(maze_dim)] # Heuristic Grid
        self.backwards = 0  # Initial value of Down direction.
        self.step_count = 0 # Number of steps taken in each trial
        self.run = 0 # Exploration or Optimization Trial
        
    def next_move(self, sensors):
        
        if self.run == 0 :
             rotation, movement = self.exploration_trial(sensors)          
        elif self.run == 1:
            rotation, movement = self.speed_racer(sensors)
        
        return rotation, movement
        
    def exploration_trial(self,sensors): 
        # Initiate Exploration Trial
        
        # Count number of steps taken
        print "Exploration Step Count: ", self.step_count, sensors
        self.step_count +=1

        # Print the robot's location         
        x1 = self.location[0]
        y1 = self.location[1]
        print "Location: ", self.location
        # Add 1 to path_grid
        self.path_grid[x1][y1] += 1
        
        # Calculate the percentage of the maze the robot has visited
        uncov = 0
        for x in range(self.maze_dim):
            for y in range(self.maze_dim):
                if self.path_grid[x][y] > 0:
                    uncov += 1

        uncovered = (uncov/self.maze_area) * 100

        print "Robot has discovered %.2f%% of the maze.\n" % uncovered
        
        # Draw the map of the maze from the sensor readings     
        num = self.wall_locations(sensors, self.backwards) 
        self.maze_grid[x1][y1] = num
        
        # Determine the robot's next move
        rotation, movement = self.determine_next_move(x1, y1, sensors)
 
        # Update the self.backwards value
        if movement == 0:
            self.backwards = 0
        elif movement == 1:
            self.backwards = 1
        elif movement == -1 or movement == -2: # Robot hit a dead end
            for move in range(2):
                if self.heading == 'l' or self.heading == 'left': # If robot is facing left, 9, 12, & 13 have a wall on right side
                    if self.maze_grid[x1+move][y1] == 9 or self.maze_grid[x1+move][y1] == 12 or self.maze_grid[x1+move][y1] == 13:
                        self.backwards = 0
                    else:
                        self.backwards = 1
                elif self.heading == 'r' or self.heading == 'right': # If robot is facing right, 3, 6, & 7 have a wall on left side
                    if self.maze_grid[x1-move][y1] == 3 or self.maze_grid[x1-move][y1] == 6 or self.maze_grid[x1-move][y1] == 7:
                        self.backwards = 0
                    else:
                        self.backwards = 1
                elif self.heading == 'u' or self.heading == 'up': # If robot is facing up, 3, 9, & 11 have a wall on bottom side
                    if self.maze_grid[x1][y1-move] == 3 or self.maze_grid[x1][y1-move] == 9 or self.maze_grid[x1][y1-move] == 11:
                        self.backwards = 0
                    else:
                        self.backwards = 1
                if self.heading == 'd' or self.heading == 'down': # If robot is facing down, 6, 12, & 14 have a wall on top side
                    if self.maze_grid[x1][y1+move] == 6 or self.maze_grid[x1][y1+move] == 12 or self.maze_grid[x1][y1+move] == 14:
                        self.backwards = 0
                    else:
                        self.backwards = 1

        # Update the robot's direction it is facing & new location
        self.update_heading(rotation, movement)
        
        # Get the new location
        x2 = self.location[0]
        y2 = self.location[1]
        
        # See if new location is in the goal.
        if x2 in self.found_goal and y2 in self.found_goal:
            if self.path_grid[x2][y2] == 0: # Don't repeat this statement
                print "*** Robot found the goal position after {} steps. ***\n".format(self.step_count)
                print "Robot still exploring."
                self.discovered_goal = True
            
        elif self.discovered_goal == True and uncovered >= 70:
            print "Robot has ended exploration. Next trial starting."
            goal = self.found_goal
            self.compute_value(goal) # Compute the value function and find optimal path
            print "\n*** Maze Grid ***\n", self.maze_grid
            print "\n*** Path Grid ***\n", self.path_grid
            print "\n*** Path Value ***\n", self.path_value
            print "\n*** Policy Grid ***\n", self.policy_grid
            
            # Restore to default settings and start Optimization Trial
            rotation = 'Reset'
            movement = 'Reset'
            self.run = 1
            self.location = [0,0]
            self.heading = 'up'
            self.step_count = 0
            self.discoverd_goal = False
            
        return rotation, movement


    def speed_racer(self,sensors):
        # Optimization Trial
    
        print "Optimization Trial Step #: ", self.step_count, sensors, self.location
        self.step_count +=1
           
        movement = 1
        
        # Retreive current location 
        x1 = self.location[0]
        y1 = self.location[1]
        
        # Rotate to the optimal path
        heading_angle = delta_degrees[self.heading]
        optimal_heading_angle = delta_degrees[self.policy_grid[x1][y1]]
        rotation = optimal_heading_angle - heading_angle
        
        # Correct for 270 degrees
        if rotation == -270:
            rotation = 90
        elif rotation == 270:
            rotation = -90
            
        # Change the angles to an index [0,1,2]    
        rot_key = rotation/90 + 1  
        direction = dir_sensors[self.heading][rot_key]  # Change direction
        
        # Move up to 3 consecutive steps
        while movement < 3: # Limit movement to 3 spaces
            location = self.policy_grid[x1][y1]
            x1 += dir_move[direction][0]
            y1 += dir_move[direction][1] 

            if self.policy_grid[x1][y1] == location:
                movement += 1      
            else: 
                break
        
        # Update direction robot is facing & location
        self.update_heading(rotation, movement)
        
        # Retrieve new location
        x2 = self.location[0]
        y2 = self.location[1]
       
        return rotation, movement

    
    def update_heading(self, rotation, movement):
        # This method updates the direction the robot is facing and its location in the maze

        # Convert rotation angles to an index key [0,1,2]
        if rotation == -90 or rotation == 270:
            rotation = 0
        elif rotation == 0 or rotation == 360:
            rotation = 1
        elif rotation == 90 or rotation == -270:
            rotation = 2
        
        # Compute new direction based upon robot's rotation
        self.heading  = dir_sensors[self.heading][rotation]
        
        # Update Location 
        self.location[0] += dir_move[self.heading][0]*movement
        self.location[1] += dir_move[self.heading][1]*movement

    def wall_locations(self, sensors, backwards):
        # Creates a binary number that represents a description of walls surrounding robot
            
        # Scales sensor reading to open or closed. 1 for open. 0 for closed. 
        # Sensor reading will be [left, front, right], so if it senses a wall, set that to 0.
        for sensor in range(len(sensors)):
            if sensors[sensor] > 0:
                sensors[sensor] = 1
                
        # 1 = North, 2 = East, 4 = South, 8 = West. Each sensor will give a reading of 1 (open) or 0 (closed)       
        if self.heading == 'u' or self.heading == 'up':
            num = (sensors[0]*8) + (backwards*4) + (sensors[2]*2) + sensors[1]
        elif self.heading =='d' or self.heading == 'down':
            num = (sensors[2]*8) + (sensors[1]*4) + (sensors[0]*2) + backwards
        elif self.heading == 'l' or self.heading == 'left':
            num = (sensors[1]*8) + (sensors[0]*4) + (backwards*2) + sensors[2]
        elif self.heading == 'r' or self.heading == 'right':
            num = (backwards*8) + (sensors[2]*4) + (sensors[1]*2) + sensors[0]
        
        return num

    def determine_next_move(self,x1,y1,sensors):
        # Determine next movement for the robot
        # Portions of the code in this method came from Udacity's Artificial Intelligence for Robotics course
        # https://www.udacity.com/course/artificial-intelligence-for-robotics--cs373
        
        # If robot runs into a dead-end, back up.
        if sensors == [0,0,0] and self.heading == 'u' and self.maze_grid[x1][y1 - 1] == 5:
            movement = -2
            rotation = 0
            print "Robot hit a deep dead end. Reversing."
        elif sensors == [0,0,0] and self.heading == 'r' and self.maze_grid[x1 - 1][y1] == 10:
            movement = -2
            rotation = 0
            print "Robot hit a deep dead end. Reversing."
        elif sensors == [0,0,0] and self.heading == 'd' and self.maze_grid[x1][y1 + 1] == 5:
            movement = -2
            rotation = 0
            print "Robot hit a deep dead end. Reversing."
        elif sensors == [0,0,0] and self.heading == 'l' and self.maze_grid[x1 + 1][y1] == 10:
            movement = -2
            rotation = 0
            print "Robot hit a deep dead end. Reversing."
        elif sensors == [0,0,0]:
            movement = -1
            rotation = 0
            print "Robot hit a dead end. Reversing."

        else: # Move to open space. Implement A*
            possible_moves = [] 
            rotate = [-90, 0, 90]
            for sensor in range(len(sensors)): # Look at all sensor readings
                if sensors[sensor] > 0: # If it has a number, that means it's open.
                    sensors[sensor] = 1  # Convert to 1 (open) or 2 (closed)
                    
                    # Move to next open space
                    x2 = x1 + dir_move[dir_sensors[self.heading][sensor]][0]   
                    y2 = y1 + dir_move[dir_sensors[self.heading][sensor]][1] 
                    
                    if x2>=0 and x2<self.maze_dim and y2>=0 and y2<self.maze_dim:    # Make sure robot next space is in maze
                        t2 = self.path_grid[x2][y2]  # Pull the number of times this cell has been visited.
                        h2 = self.heuristic[x2][y2]  # Small number means close to the goal area.
                        possible_moves.append([t2,h2,x2,y2,sensor]) # Create a list of the possible moves
                        
            possible_moves.sort()
            possible_moves.reverse()
            min_move = possible_moves.pop()  # Move to cell that is closest to the center and/or hasn't been explored.
            
            t,h,x,y,sensor = min_move # Break it up into separate variables
            rotation,movement = rotate[sensor], 1  # Rotate to opening and move 1 space.

        return rotation, movement                    
         

    def compute_value(self, goal):
        # Dynamic Programming Method using a Value Function
        # Portions of the code in this method came from Udacity's Artificial Intelligence for Robotics course
        # https://www.udacity.com/course/artificial-intelligence-for-robotics--cs373
    
        change = True   # Initialize boolean to start while-loop  
        
        while change:
            change = False  # Stop if nothing has changed
            
            for x in range(self.maze_dim):
                for y in range(self.maze_dim):                                       
                    if goal[0] == x and goal[1] == y:                        
                        if self.path_value[x][y] > 0: # Prevent endless loop
                            self.path_value[x][y] = 0 # Assign 0 to goal position
                            self.policy_grid[x][y] = '*' # Assign * to goal position
                            print "Goal location: {}\n".format(goal)
                            
                            change = True
                    else:                        
                        # Convert the wall value into a 4-bit number 
                        wall = self.maze_grid[x][y]
                        binary = int(bin(wall)[2:])
                        four_bit = '%0*d' % (4,binary)

                        # Start at goal and increase incrementally by 1 in open spaces
                        for direction in range(len(delta)): 
                            if (four_bit[0] == '1' and direction == 0) or (four_bit[1] == '1' and direction == 1) or (four_bit[2] == '1' and direction == 2) or (four_bit[3] == '1' and direction == 3):
                            # four_bit = 0000 = left,down,right,up Direction = left,down,right,up
                                x2 = x + delta[direction][0]
                                y2 = y + delta[direction][1]

                                if x2 >= 0 and x2 < self.maze_dim and y2 >= 0 and y2 < self.maze_dim:    # Make sure inside maze
                                    v2 = self.path_value[x2][y2] + 1   # Add 1 to path value
                                    
                                    if v2 < self.path_value[x][y]:
                                        change = True
                                        self.path_value[x][y] = v2 # Update path_value with new count number
                                        self.policy_grid[x][y] = delta_name[direction]  # Add movement symbol to policy_grid (<, v, >, or ^)
              