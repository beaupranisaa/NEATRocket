# NEATLanding
A rocket controller using NEAT.

### TODO:

- [x] Convert the rockets into objects
- [x] Change base to static shape object
- [ ] Create a fitness funtion
- [ ] Create a configuration file
- [ ] Create a neat.config.Config object from the configuration file.
- [ ] Create a neat.population.Population object using the Config object created above.
- [ ] Call the run method on the Population object, giving it your fitness function and (optionally) the maximum number of generations you want NEAT to run.

### Dependencies:

1. pymunk
2. pyglet
3. neat-python

### Usage:

```python
python3 manual.py # to manually play the game
python3 neat.py # to let the NN play the game
```

Use the up arrow key for the main thrust.
Use the left and right arrow keys for the side boosters. 

### NEAT Setup

Every generation will have 10secs to reach the desired state. 

- States/Input:
    - x error = current x position - desired x position
    - y error = current y position - desired y position
    - a error = current angular position - desired angular position
    - vx error = current x velocity - desired x velocity
    - vy error = current y velocity - desired y velocity
    - va error = current angular velocity - desired angular velocity
- Output:
    - longitudinal thrust states: [0,+1]
    - top lateral booster states: [-1,+1]
    - bottom lateral booster states: [-1,+1]
- fitness function : Summation of L2 norm of the states across time
    - When rocket leaves the screen we set the current state to the position the object left, and multiply the remaining time with the exit position to get the fitness function
- fitness criterion = min
- fitness threshold = ? 
