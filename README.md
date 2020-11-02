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

