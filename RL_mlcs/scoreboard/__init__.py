import os

from gym.scoreboard.registration import registry, add_task, add_group

add_group(
    id='gazebo',
    name='Gazebo',
    description='TODO.'
)

add_task(
    id='test-v0',
    group='gazebo',
    summary='Obstacle avoidance in a Circuit.',
)

add_task(
    id='factory-v0',
    group='gazebo',
    summary='Obstacle avoidance in a Factory.',
)

registry.finalize()
