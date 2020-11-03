# NEATRocket
A rocket controller using NEAT.

### Dependencies:

1. pymunk 5.7.0
2. pyglet 1.5.7
3. neat-python 0.92

### Usage:

```python
python3 manual.py # to manually play the game
python3 train.py # to train the NN
python3 auto.py # to run the trained NNs
```

### NEAT Setup

- States/Input:
    - x error = current x position - desired x position
    - y error = current y position - desired y position
    - a error = current angular position - desired angular position
    - vx error = current x velocity - desired x velocity
    - vy error = current y velocity - desired y velocity
    - va error = current angular velocity - desired angular velocity
- Output:
    - longitudinal thrust states: [-1,+1]
    - top lateral booster states: [-1,+1]
    - bottom lateral booster states: [-1,+1]
- fitness function : Summation of weighted squared errors of states across time
    - Every generation will have 10secs to reach the desired state. 
    - When rocket leaves the screen we set the current state to the position the object left, and multiply the remaining time with the exit position to get the fitness function
