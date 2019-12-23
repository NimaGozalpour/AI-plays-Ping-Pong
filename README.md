# AI-plays-Ping-Pong

In this project which is deployed in python 3, the goal is creating an AI can play Ping-Pong game. In addition, the game is 2d ping-pong simulation, created by pygame library, and it continues until the racket saves the ball. AI controls the racket and contains a three-layer neural network, first layer has two input, one of them is distance of the ball from middle of the racket in x axis and another one in y axis. Second layer has 10 neurons and last one has just one. Former and latter layers’ activation function are sigmoid and linear, respectively. Finally, Genetic Algorithm finds appropriate weights for the neural network in order to save any ball. For this purpose, fitness of each chromosome is number of saved balls. Also, initial population is 10 and in other generations, 4 best chromosomes from previous generation is copied and 6 children from them are produced using crossover and mutation.
## Getting Started

For running this code, you must have python 3 on your machine and pygame and numpy libraries must be installed on python.

### Prerequisites

Platform:
Python 3

Used libraries: pygame, time, random, numpy, math.

## Authors

* **Nima Gozalpour** - *Initial work* - [NimaGozalpour](https://github.com/NimaGozalpour)

