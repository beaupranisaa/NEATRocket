# NEATRocket

Training a rocket controller using the NEAT algorithm.

### Dependencies:

1. pymunk 5.7.0
2. pyglet 1.5.7
3. neat-python 0.92

### Usage:

- Manually control the rocket with your arrow keys.

```shell
$ python3 manual.py
```

- Train the network

```shell
$ python3 train.py <name of the directory to save the neural networks to (optional)>

#Example
$ python3 train.py networks/
```

- Automatic rocket control

```shell
$ python3 auto.py <neural network files (optional)> 

# Example:
$ python3 auto.py networks/* networks2/Net_0.p
```
- Remove all networks

```shell
$ bash clear.sh
```

### NEAT Setup

- **States/Input:**
    - x error = current x position - desired x position
    - y error = current y position - desired y position
    - a error = current angular position - desired angular position
    - vx error = current x velocity - desired x velocity
    - vy error = current y velocity - desired y velocity
    - va error = current angular velocity - desired angular velocity
- **Output:**
    - longitudinal propulsion states: clamped [-1,+1]
    - top lateral propulsion states: clamped [-1,+1]
    - bottom lateral propulsion states: clamped [-1,+1]
- **fitness function** : Summation of weighted squared errors of the positional states across time

### Todo:

- [ ] Add text and visualizations (best genome is a space shuttle, list of fitness, generation number, identification for each genome)
- [x] Find better fitness functions
- [x] Read the paper again.
- [x] Optimize config file
- [ ] Record and make presentation
    - find interesting points







