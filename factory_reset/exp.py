from env_reset import env_reset
from tqdm import tqdm

env_reset().gazebo_warmup()

for i in tqdm(range(0,10)):
    env_reset().rand_deploy()
    env_reset().rand_remove()