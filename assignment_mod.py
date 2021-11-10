from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance """

d_th = 0.4
""" float: Threshold for the control of the orientation """

m_th = 0.8
""" float: Threshold for the control of collisions """

R = Robot()
""" instance of the class Robot """

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def find_token():
    """
    Function for finding the closest token.

    Returns:
    	-dist(float): the value of the distance of the closest token [-1 if no token are finding];
    	-rot_y(float): the value of the angle between the robot and the closest token [-1 if no token are finding];
    	-token_colour(string): the colour of the closest token (in our case the colour can be silver or golden) [-1 if no token 					are finding].
    The tokens are searched in the interval in front of the robot bounded between -60 and +60 degrees.
    """
    
    dist=100
    for token in R.see():
        if token.dist < dist and -60 < token.rot_y < 60:
            dist=token.dist
            rot_y=token.rot_y
    	    token_color=token.info.marker_type 
    if dist==100:
	return -1, -1, -1
    else:
    	return dist, rot_y, token_color
   	
def find_silver_token():
    """
    Function, similar to the 'find_token', which returns the same value of the previous function, except the colour of the      	 token. Infact, in this function, we are searching only silver token.
    Tokens are searched only in the semi-plane in front of the robot (-90 < token.rot_y < 90)
    """
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -90 < token.rot_y < 90:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
def find_golden_token():
    """
    Function indentical to the 'find_silver_token', excepts the fact that the sought token now are golden. 
    Also in this case the tokens are searched only in the semi-plane in front of the robot (-90 < token.rot_y < 90).
    """
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45 < token.rot_y < 45:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
   		
def find_golden_token_right():
    """
    Useful function to avoid the collisions with the walls of the arena. It is called when the front distance between the      	robot and the wall falls below a certain threshold.
    
    Returns:
    	-dist(float): distance between the robot and the closest golden token on the right [-1 if no token are finding];
    [Values are calculated with 75 < token.rot_y < 105].
    """
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75 < token.rot_y < 105:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
   	
def find_golden_token_left():
    """
    Useful function to avoid the collisions with the walls of the arena. It is called when the front distance between the      	robot and the wall falls below a certain threshold. 
    
    Returns:
    	-dist(float): distance between the robot and the closest golden token on the left [-1 if no token are finding];
    [Values are calculated with -105 < token.rot_y < -75].
    """
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105 < token.rot_y < -75:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
   	
def avoid_collision(dist):	
	"""
	Function useful for avoid the collisions between the robot and the wall of the arena and also to rightly follow the 	path desired. It use the function 'find_golden_token_left' and 'find_golden_token_right' to choose the right direction 		to turn (the robot turns to the side where the distance (between right and left) obtained from the two functions is 	greater) when the distance between the robot and the wall falls under the threshold (0.8).
	If the distance between the robot and the wall is greater than the threshold, the robot go forward.
	
	"""
	dist_R = find_golden_token_right() # value of distance and angle to the closest token on the right.
	dist_L = find_golden_token_left() # value of distance and angle to the closest token on the left.
	
	if dist < m_th: # if we are too close to the wall we have to turn
		print("The value of the right distance is:", dist_R, "the value of the left distance is:", dist_L) 
		if dist_R > dist_L: # if the right wall is further away than the left one we have to turn right.
			while dist < m_th:
				print("Turn right")
				turn(5,0.5)
				dist = find_golden_token()
		else: 	            # if the right wall is closer than the left one we have to turn left.
			while dist < m_th:
				print("Turn left")
				turn(-5,0.5)
				dist = find_golden_token()
	else:           # else if we are not too close to the wall we can go forward.
		drive(20,1) 
		print("Go forward!")
		
def take_silver_token():
    """
    Function for bring the silver token 180 degrees behind.
    """
    while True:
    	    dist, rot_y = find_silver_token() # after each iteraction we calculate the values of distance and angle between the 	                                             robot and the silver token
	    if dist < d_th:  # when the robot is close to the silver token
		print("Found it!") 
		if R.grab(): # if we are close to the token, we grab it. 
			dist_R = find_golden_token_right()
			dist_L = find_golden_token_left()
			print("Gotcha!")
			if dist_R < m_th:  # if the silver token is close to the wall it turns left
				turn(-20, 3) # put the token 180 degrees behind
				print("Release the silver token") 
				R.release()
				drive(-10,1.5) 
				turn(20, 3) # the robot returns to the path taken previously
			else:               # else the distance between the robot and the wall is greater than the thresold we   						       can turn right
				turn (20,3)
				print("Release the silver token")
				R.release()
				drive(-10,1.5)
				turn(-20,3)
			return # after the grab part exit from this function
	    elif dist >= d_th:
		if -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward 
		    print("Ah, here we are!.") 
		    drive(20, 0.1) 
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right 
		    print("Left a bit...") 
		    turn(-1, 0.5) 
		elif rot_y > a_th: 
		    print("Right a bit...") 
		    turn(+1, 0.5) 
		    
def main():
	"""
	In the main function we analyze the colour of the closest token and based on it we call the correct function.
	The program goes on until an interrupt by keyboard.
	"""
	while True:
		dist, rot_y, token_color = find_token() # gets the value of the distance and the angle between the robot and    					                     the closest token and also its colour.
		
		if token_color is MARKER_TOKEN_GOLD: # if the token is golden we have call the function that avoids collisions
			avoid_collision(dist)         # beetween the robot and these tokens.
			
		elif token_color is MARKER_TOKEN_SILVER: # otherwise if the token is silver we have call the function that
 		        take_silver_token()               # grab it and turns it 180 degrees behind              
			

main()
