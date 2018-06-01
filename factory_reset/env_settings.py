import os

class env_settings(object):
    def __init__(self):
        self.gazebo_model_path = os.path.dirname(os.path.realpath(__file__))+'/models/'
        self.tool_pop_desired = 7 #Desired total machine tool population

        self.floor_list = ['blue', 'darkgrey', 'darkred', 'green', 'lightgrey', 'urethane']
        self.wall_list = ['brownbrick', 'concrete', 'grey', 'oldbrick', 'redbrick']
        self.tool_list = ['lathe', 'systec']

        self.floor_texture_num = len(self.floor_list) #Number of the floor type
        self.wall_texture_num = len(self.wall_list) #Number of the wall type
        self.tool_num = len(self.tool_list) #Number of the machine tool type

        self.x_length = 25 #Factory x direction length
        self.y_length = 25 #Factory y direction length


env_config = env_settings()