import math

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    reward = 1
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    is_left_of_center = params['is_left_of_center']
    all_wheels_on_track = params['all_wheels_on_track']
    steering_angle = params['steering_angle']
    is_reversed = params['is_reversed']
    is_crashed = params['is_crashed']
    is_offtrack = params['is_offtrack']
    speed = params['speed']
    x = params['x']
    y = params['y']
    
    
    if(is_reversed or is_crashed):
        reward = 1e-3
        return float(reward)
    
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
        
    if abs(direction_diff - heading) < abs(direction_diff - (heading + steering_angle)):
        reward *= 0.4
    else:
        reward *= 1.1
    
    
    my_direction = math.atan2(next_point[1] - y, next_point[0] - x)
    my_direction = math.degrees(my_direction)
    my_diff = abs(my_direction - heading)
    if my_diff > 180:
        my_diff = 360 - my_diff
        
    if abs(my_diff - heading) < abs(my_diff - (heading + steering_angle)):
        reward *= 0.2
    else:
        reward *= 1.3
        
    if not all_wheels_on_track:
        reward *= 0.05
    
    if abs(my_diff - (heading + steering_angle)) < 6 and speed < 1.5:
        reward *= 0.8
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.35 * track_width
    marker_3 = 0.46 * track_width
    
    if distance_from_center >= marker_3:
        reward *= 0.15
    elif distance_from_center <= marker_2:
        reward *= 1.2
    
    return float(reward)
