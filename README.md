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

### Fitness Function

### Fitness Function

Every generation will have 10secs to reach the desired state. 

- summation of L^2 distance between current state and desired state across time
    - when rocket leaves the screen we set the current state at the position the object left, and multiply the remaining time with the exit position
- fitness criterion = min
- fitness threshold = ? 
