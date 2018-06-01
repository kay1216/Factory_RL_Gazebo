import subprocess
import time
import numpy as np
import math
import commands
from env_settings import env_config

##check '$roscore & rosrun gazebo_ros gazebo'

class env_reset(object):
    def __init__(self):
        self.gazebo_model_path = env_config.gazebo_model_path
        self.tool_pop_desired = env_config.tool_pop_desired

        self.floor_list = env_config.floor_list
        self.wall_list = env_config.wall_list
        self.tool_list = env_config.tool_list

        self.floor_texture_num = env_config.floor_texture_num
        self.wall_texture_num = env_config.wall_texture_num
        self.tool_num = env_config.tool_num

        self.x_length = env_config.x_length
        self.y_length = env_config.y_length

    ### Warning: Checking makes whole reset process slow down.

    # def del_check(self, ind):
    #     while commands.getstatusoutput('rosservice call /gazebo/get_model_properties \"{model_name: tool'+str(ind)+'}\"')[1].find('success: False') == -1:
    #         time.sleep(3)

    # def spawn_check(self, ind):
    #     while commands.getstatusoutput('rosservice call /gazebo/get_model_properties \"{model_name: tool'+str(ind)+'}\"')[1].find('success: True') == -1:
    #         time.sleep(3)

    def rand_deploy(self):
        np.random.seed(int(math.floor(time.time())))
        subprocess.call('rosservice call gazebo/reset_simulation',shell=True)
        floor_choose = math.floor(np.random.random(1)*(self.floor_texture_num))
        wall_choose = math.floor(np.random.random(1)*(self.wall_texture_num))
        
        x = np.random.randint(self.x_length, size=self.tool_pop_desired)
        y = np.random.randint(self.y_length, size=self.tool_pop_desired) 

        subprocess.call('rosrun gazebo_ros spawn_model -file ' + self.gazebo_model_path +'buildings/'+ self.floor_list[int(floor_choose)]+'_floor/model.sdf -sdf -model floor -y {0} -x {1}'.format(0,0), shell=True)
        
        subprocess.call('rosrun gazebo_ros spawn_model -file ' + self.gazebo_model_path +'buildings/'+ self.wall_list[int(wall_choose)]+'_wall/model.sdf -sdf -model wall -y {0} -x {1}'.format(0,0), shell=True)
        
        for i in range(0,self.tool_pop_desired):
            tool_choose = math.floor(np.random.random(1)*(self.tool_num))
            subprocess.call('rosrun gazebo_ros spawn_model -file ' + self.gazebo_model_path + self.tool_list[int(tool_choose)]+'/model.sdf -sdf -model tool{0} -y {1} -x {2}'.format(str(i+1),x[i],y[i]), shell=True)
            #self.spawn_check(i+1)
        
        print('-'*50 +'\n Randomized environment model set done.')

    def rand_remove(self):
        subprocess.call('rosservice call gazebo/delete_model \'{model_name: floor}\'',shell=True)
        subprocess.call('rosservice call gazebo/delete_model \'{model_name: wall}\'',shell=True)
        for i in range(0,self.tool_pop_desired):
            subprocess.call('rosservice call gazebo/delete_model \'{model_name: tool'+str(i+1)+'}\'', shell=True)
            #self.del_check(j)

        print('-'*50 +'\n Randomized environment model delete done.')

    def gazebo_warmup(self):
        for i in range(0, self.tool_num):
            subprocess.call('rosrun gazebo_ros spawn_model -file ' + self.gazebo_model_path + self.tool_list[i] +'/model.sdf -sdf -model warmup_tool{0} -y 0 -x 0'.format(i+1), shell=True)
        time.sleep(60)
        for i in range(0, self.tool_num):
            subprocess.call('rosservice call gazebo/delete_model \'{model_name: warmup_tool'+str(i+1)+'}\'', shell=True)


        