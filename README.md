Research Track1 - First Assignment
================================
Stefano Molinari 4703592

The first assignment consists on the development of a software program, written in python language, which drives the robot around the desired path.

The robot in the path must not collide with the walls, represented with the golden token, and must grab the silver tokens bringing them 180 degrees behind.

This program is based on the `R.see` method, which makes the robot doing things written before.

The program should be able to:

  * drives the robot around the circuit in the counter-clockwise direction;
 
  * makes the robot avoid the golden tokens, which constitute the 'walls' of the circuit;
 
  * drives the robot close to the nearest silver box, it should grab it, and moves it behind itself.

 ![MicrosoftTeams-image](https://user-images.githubusercontent.com/62506638/141134541-16f0ce08-04f9-4e52-8af7-bfbed80f3cc0.png)


Running 
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

To run this script in the simulator, use `run.py`, passing it the file names. 

```bash
$ python2 run.py assignment.py
```

Robot Behaviour
----------------------

After running the script, the robot and arena will appear to you in a enviroment pre-built, in which the robot, thanks to the color code of the token, can distinguish the color of the token (in our case we only have two differents possible color of the tokens: silver and gold). Also the robot is generated after the running of the script, and it begins its counterclock-wise drives, detecting the distance and  the angle between it and the closest token, in addition to the color of it. Now, the robot, being aware of the closest token's color knows how to behave. In fact, if the color of the closest token is golden, the robot knows the distance from it and if this distance is greater than a certain threshold (fixed in this program at 0.8) it goes forward. When the distance from the golden token falls down the threshold, the robot turns around, so as to avoid the collision with the token/wall. When the robot detects a silver token, it has to align with this. After the alignment the robot has to reach (very close) the silver token and grab it. After grabbing the token, the robot has to turn the token 180 degress behind and after release the token, returning to the path taken before the grabbing, in order to continue its counterclockwise path.

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

### Software Architecture ###
----------------------

For this script I have implemented 9 different functions, beyond the main function.
Now I explain in few lines each function.

### Drive function ###

The drive function is used to set the linear speed of the robot. This function used two motors of the class Robot, and sets to each one the same speed (chosen by the programmer) and a time of use, expressed in second. For the establish time the robot goes forward and after this the robot stops.

This function has two parameters: speed [int] and seconds(time) [int].

### Turn function ###

The turn function is used to make the robot turns. This function used the same two motors of the previous analyzed function, but in this case one of these motors is set with a positive speed and the other one with the same speed but negative (the moduls of the two speed is the same, with opposite sign). In this function the time of use must be set as well, and during this time the robot turns, stopping after it.

Thanks to this function the programmer can make the robot turns to left or right as desired.

This function has two parameters: speed [int] and seconds(time) [time].

### Find_Token function ###

With the 'find_token' function the robot can see every token in the arena but returns only the value of the closest one. The values returned are the distance and the angle from it, in addition to the color. This is used in the main for calls the right function if the color of the closest token is silver or golden.

In case of a silver token the robot has to reach it and grab it, in the other case (golden token) the robot has to avoid the collision with it.

```python
def find_token():
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
```
### Find_Silver_Token function ###

The 'find_silver_token' is only looking for silver tokens and returns to the value of distance and angle of the closest one. 

It is used to update, at every iteration of the while of the 'take_silver_token', the distance and the angle between the robot and the closest silver token.

This function calculates the distance and the angle only for the silver tokens. 

This function has no parameter passed.

```python
def find_silver_token():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -90 < token.rot_y < 90:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
            return -1, -1
    else:
    return dist, rot_y
```
### Find_Golden_Token function ###

The 'find_golden_token' searching only for the golden tokens and returns only the value of the distance of the closest one. 

It is used to update, at every iteration of the whiles of the 'avoid_collision', the distance of the closest golden token after the turn to have a control if the turn was enough. 

This function calculates only the distance of the closest golden token.

This function has no parameter passed.

```python
def find_golden_token():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45 < token.rot_y < 45:
            dist=token.dist
    if dist==100:
         return -1
    else:
         return dist
```

### Dist_Wall_Right function ###

The 'find_golden_token_right' is used to avoids the collisions between the robot and the walls of the circuit, represented by the golden tokens.

This function calculates (and returns to the function 'avoid_collision') the value of the distance of the closest golden token at the right of the robot. 

This function has no parameter passed.

```python 
def find_golden_token_right():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75 < token.rot_y < 105:
            dist=token.dist
    if dist==100:
        return -1
    else:
        return dist
```

### Dist_Wall_Left function ###

The 'find_golden_token_left' is used to avoids the collisions between the robot and the walls of the circuit, represented by the golden tokens.

This function calculate (and returns to the function 'avoid_collision') the value of the distance of the closest golden token at the left of the robot. 

This function has no parameter passed.

```python 
def find_golden_token_left():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105 < token.rot_y < -75:
            dist=token.dist
    if dist==100:
        return -1
    else:
        return dist
```

### Avoid_Collision function ###

The 'avoid_collision' function is used to avoid the collisions between the robot and the walls of the circuit, represented by the golden tokens. 

In it we check if the distance of the robot and the golden token is greater of a certain threshold(m_th). If this is verificated the robot can go forward, otherwise, if this isn't the robot has to turn around. The part where the robot has to turn is determinated by the farest wall, calculated thanks to the functions 'dist_wall_left' and 'dist_wall_right'. When the distance of the robot from the closest golden token is bigger than the threshold, it stops its turning and return to go forward until it will be close enough to an other golden token.

This function has only one parameter passed: the distance of the closest token (it will be updated after every iteraction of the whiles)

```python
def avoid_collision(dist): 
  if dist < m_th: # if we are too close to the wall we have to turn
    dist_R = dist_wall_right() # value of distance and angle to the closest token on the right.
    dist_L = dist_wall_left() # value of distance and angle to the closest token on the left.
    print("The value of the right distance is:", dist_R, "the value of the left distance is:", dist_L) 
    if dist_R > dist_L: # if the right wall is further away than the left one we have to turn right.
          while dist < m_th:
          print("Turn right")
          turn(5,0.5)
          dist = find_golden_token()
    else:              # if the right wall is closer than the left one we have to turn left.
          while dist < m_th:
          print("Turn left")
          turn(-5,0.5)
          dist = find_golden_token()
  else:           # else if the robot is not close enough to the wall it can go forward.
          drive(20,1) 
          print("Go forward!")
```

### Take_Silver_Token function ###

The 'take_silver_token' is used to grab the silver tokens.

If the distance between the robot and the silver token is bigger than the threshold(d_th), it has to reach the token. If the robot and the token are well aligned the robot has only to go forward until it reaches the silver token; otherwise, if the robot is not aligned well with the token, before going forward, it has to turn until the alignment is good. 

When the robot reaches the silver token with a good alignment the robot has to grab it and turn it 180 degrees behind. When the robot grabs the token it checks if the wall on the right isn't too close and if the wall isn't close enough the robot can turn right to bring the silver token 180 degrees behind; otherwise, if the wall is close, the robot turns left to bring the silver token 180 degrees behind. After bringing the silver token 180 degrees behind, the robot releases the token and returns (with the same speed, with  opposite sign, and for the same time, to the previous turn) on the path taken previously (the counterwiseclock path).

This function has no parameter passed.

```python
def take_silver_token():
    while True:
         dist, rot_y = find_silver_token() # after each iteraction we calculate the values of distance and angle between the robot and the silver token
      if dist < d_th:  # when the robot is close to the silver token
            print("Found it!") 
            if R.grab(): # if we are close to the token, we grab it. 
                 dist_R = dist_wall_right()
                 dist_L = dist_wall_left()
                 print("Gotcha!")
                 if dist_R < m_th:  # if the silver token is close to the right wall it turns left
                        turn(-20, 3) # put the token 180 degrees behind
                        print("Release the silver token") 
                        R.release()
                        drive(-10,1.5) 
                        turn(20, 3) # the robot returns to the path taken previously
                 else:               # if the distance between the robot and the wall is greater than the thresold we can turn right
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
```

### Main Function ###

def main():
 while True:
     dist, rot_y, token_color = find_token() # gets the value of the distance and the angle between the robot and                                    the closest token and also its colour.
  
     if token_color is MARKER_TOKEN_GOLD: # if the token is golden we have to call the function to avoid collisions
           avoid_collision(dist)         # beetween the robot and these tokens.
   
    elif token_color is MARKER_TOKEN_SILVER: # otherwise if the token is silver we have to call the function that
           take_silver_token()              # makes the robot grab it and turns it 180 degrees behind              

### Pseudocode ###

```python
while true

     find the closest token and calculate the distance, angle and color
 
     if the token color is golden
           if the robot and the token are close
                 calculate the distance of the right and left wall 
                 print "The right distance is (distR) and the left distance is (distL)"
                 if the right distance is greater than the left one
                            turn right until the distance of the robot from the wall is greater than the threshold
                 else
                            turn left until the distance of the robot from the wall is greater than the threshold
           else
                 drive forward
   
     if the token color is silver
 
            while true
                 update the coordinates of distance and angle of the silver token
                 if distance is lower than the threshold
                             print "Found it!"
                             when the robot now has grabbed the token
                                      print "Gotcha"
                                      calculate the distances of right and left wall
                                      if the robot is close to the right walls
                                                   turn left to bring the token 180 degrees behind
                                                   release the token
                                                   drive behind
                                                   turn right to retake the previous path
                                     else
                                                   turn right to bring the token 180 degrees behind
                                                   release the token
                                                   drive behind
                                                   turn right to retake the previous path
                 else
                           if the robot is well aligned with the silver token
                                           drive until the robot reaches that
                                           print "Ah, he we are!"
                           else 
                                          if the robot is misaligned to the left
                                                 turn right
                                                 print "Turn right a bit..."
                                          else (the robot is misaligned to the right)
                                                 turn left
                                                 print "Turn left a bit.."
```

### Possible Future Developments ###
----------------------

The implemented code to make the robot doing what we desired works for most of time, but, rarely, the robot turns in the wrong direction and doesn't go on the desired path. 
This happen because in some of the circuit's vertices the distance between the right wall and the left wall is not calculated correctly and so the robot turns on the wrong way.
With another program, more complicated than this one, with more controls over the path taken by the robot, this rare bug can be fixed. 

