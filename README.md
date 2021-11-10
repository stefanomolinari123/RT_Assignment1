Research Track1 - First Assignment
================================
Stefano Molinari 4703592

The first assignment consist in the development of a software program, written in python language, which drives the robot around the desired path.

The robot in the path must not collide with the walls, represented with the golden token, and must grab the silver token bringing them 180 degress behind.

This program is based on the `R.see` method, which makes the robot do things written before.

The program should be able to:

  * drives the robot around the circuit in the counter-clockwise direction;
 
  * make the robot avoid avoid the golden tokens, which constitute the 'walls' of the circuit;
 
  * drives the robot close to the closest silver box, it should grab it, and move it behind itself.

 ![MicrosoftTeams-image](https://user-images.githubusercontent.com/62506638/141134541-16f0ce08-04f9-4e52-8af7-bfbed80f3cc0.png)


Running 
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

To run this script in the simulator, use `run.py`, passing it the file names. 

```bash
$ python2 run.py assignment.py
```

Robot Behaviour
---------

After running the script, the robot and arena will appear you in a enviroment pre-build in which the robot, thanks to the color code of the token, can distinguish the color of the token (in our case we have only two different possible color of the tokens: silver and golden). Also the robot is generated after the running of the script, and begins its counterclockwise drives detecting the distance and  the angle between them and the closest token, in addition to the color of it. Now, the robot, following the closest token color knows how to behave. In fact, if the color of the closest token is golden, it compare the distance from it and if this distance is greater than a certain threshold (fixed in this program at 0.8) it goes forward. When the distance from the golden token falls down the threshold, it turns, so as to avoid the collision with the token/wall. When the robot detects a silver token, it has to align with this. After this alignment the robot has to reach (very close) the silver token and grab it. After the grab the robot has to turn the token 180 degress behind and after release them, returning to the path takes before the grabbing, in order to continue its counterclockwise path.

[VIDEO COMPORTAMENTO]

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
### ----------------------- ###

For this script I have implemented 9 different functions, beyond function main().
Now I explain in few lines each function.

### Drive function ###

The drive function is used to set the linear velocity of the robot. This function used two motors of the class Robot, and sets to each one the same velocity (chosen by the programmer) and a time of use, expressed in second. For the establish time the robot goes forward and after this the robot stops.

This function has two parameters: speed [int] and seconds(time) [int].

### Turn function ###

The turn function is used to make the robot turns. This function used the same two motors of the previous analyzed function, but in this case one of this motors is set with a positive velocity and the other one with the same velocity but negative (the moduls of the two velocity is the same, only the sign of that is negative). Also in this function the time of use must be set.

Thanks to this function the programmer can make the robot turns to left or right as desired.

This function has two parameters: speed [int] and seconds(time) [time].

### Find_Token function ###

With the 'find_token' function the robot can sees every token in the arena but returns only the value of the closest one. The values returned are the distance and the angle from it, in addition to the color of the token. This is used in the main for calls the right function if the color of the closest token is silver or golden.

In case of a silver token the robot has to reach them and grab it, in the other case (golden token) the robot has to avoid the collision with it.

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

The 'find_silver_token' searching only for silver tokens and returns the value of distance and angle of the closest one. 

It is used for refresh, at every iteration of the while of the 'take_silver_token', the distance and the angle between the robot and the closest silver token. In fact, this function calculates the distance and the angle only for the silver token. 

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

It is used for refresh, at every iteration of the whiles of the 'avoid_collision', the distance of the closest golden token after the turn to have a control if the turn was enough. 

This function calculate only the distance of the closest golden token.

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

### Find_Golden_Token_Right function ###

The 'find_golden_token_right' is used for avoids the collisions between the robot and the walls of the circuit, represented by the golden tokens.

This function calculate (and returns to 'avoid_collision') the value of the distance of the closest golden token at the right of the robot. 

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

### Find_Golden_Token_Left function ###

The 'find_golden_token_left' is used for avoids the collisions between the robot and the walls of the circuit, represented by the golden tokens.

This function calculate (and returns to 'avoid_collision') the value of the distance of the closest golden token at the left of the robot. 

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

The 'avoid_collision' function is used for avoid the collisions between the robot and the walls of the circuit, represented by the golden tokens. 

In it we check if the distance of the robot and the golden token is greater of a certain threshold(m_th). If this is verificated the robot can go forward, otherwise, if this isn't verificated the robot has to turn. The part where the robot has to turn is determinated by the farest wall, calculated thanks to 'find_golden_token_left' and 'find_golden_token_right'. When the distance of the robot from the closest golden token is bigger than the threshold it stops its turning and return to go forward until it will be too close to a golden token.

This function has only one parameter passed: the distance of the closest token (it will be refreshed after every iteraction of the whiles)

```python
def avoid_collision(dist): 
 if dist < m_th: # if we are too close to the wall we have to turn
  dist_R = find_golden_token_right() # value of distance and angle to the closest token on the right.
  dist_L = find_golden_token_left() # value of distance and angle to the closest token on the left.
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
 else:           # else if we are not too close to the wall we can go forward.
  drive(20,1) 
  print("Go forward!")
```

### Take_Silver_Token function ###

The 'take_silver_token' it used for grabbing the silver token.

If the robot is farest than the threshold(d_th) from the silver token, it have to reach that. If the robot and the token are well aligned the robot has only to go forward until it reaches the silver token; otherwise, if the robot are bad aligned the robot before go forward has to turn until the alignment is good. 

When the robot reaches the silver token with a good alignment the robot has to grab it and turn it 180 degrees behind. When the robot grabs the token it checks if the right wall is too close for the turn and if isn't the robot can turn right for bringing the silver token 180 degrees behind; otherwise, if the wall is close the robot turns left for bringing the silver token 180 degrees behind. After bringing the silver token 180 degrees behind, the robot releases the token and returns (with a turn with the same velocity, with the opposite sign, and for the same time, to the previous turn) on the path taken previously (the counterwiseclock path).

This function has no parameter passed.

```python
def take_silver_token():
    while True:
         dist, rot_y = find_silver_token() # after each iteraction we calculate the values of distance and angle between the                                               robot                                              and the silver token
     if dist < d_th:  # when the robot is close to the silver token
  print("Found it!") 
  if R.grab(): # if we are close to the token, we grab it. 
   dist_R = find_golden_token_right()
   dist_L = find_golden_token_left()
   print("Gotcha!")
   if dist_R < m_th:  # if the silver token is close to the right wall it turns left
    turn(-20, 3) # put the token 180 degrees behind
    print("Release the silver token") 
    R.release()
    drive(-10,1.5) 
    turn(20, 3) # the robot returns to the path taken previously
   else:               # else the distance between the robot and the wall is greater than the thresold we                can turn right
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

