# Global variables/dictionaries from tester.py 
dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
            'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}

# delta = Left, Down, Right, Up
delta = [[-1,0],[0,-1],[1,0],[0,1]]

delta_degrees = {'up': 0,'left': -90,'right':90, 'down':180,'u': 0,'l': -90,'r':90, 'd':180, 
				 '^': 0, '<': -90, '>': 90, 'v': 180}

delta_name = ['<','v','>','^']

#path_symbol = {'up': '^','left': '<','right':'>', 'down':'v','u':'^','l': '<','r':'>', 'd':'v'}

