# Predator-Prey Model

## Summary

A simple ecological model, consisting of three agent types: Predators, Prey, and GrasPatches. The Predators and Prey wander around the grid at random. Predators and Prey both expend energy moving around, and replenish it by eating. Prey eat GrassPatches, and Predators eat Prey if they end up on the same grid cell.

If wolves and sheep have enough energy, they reproduce, creating a new wolf or sheep (in this simplified model, only one parent is needed for reproduction). The grass on each cell regrows at a constant rate. If any wolves and sheep run out of energy, they die.

The model is tests and demonstrates several Mesa concepts and features:
- MultiGrid
- Multiple agent types
- Overlay arbitrary text on agent's shapes while drawing on CanvasGrid
- Agents inheriting a behavior (random movement) from an abstract parent
- Writing a model composed of multiple files.
- Dynamically adding and removing agents from the schedule


## Further Reading

This model is closely based on the NetLogo Wolf-Sheep Predation Model:

Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

See also the [Lotka–Volterra equations
](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) for an example of a classic differential-equation model with similar dynamics.


### Install from Terminal:

Linux boot Predator-Prey:
```bash
conda activate mesa_pd
pip install git+https://github.com/doesburg11/mesa_pd.git
cd /home/doesburg/DataspellProjects/mesa_pd
#kill the server if occupied
kill -9 $(ps -A | grep python | awk '{print $1}')
mesa runserver predator_prey
```
Windows boot Predator-Prey:
```bash
cd C:\Users\peter\OneDrive\python\pd\mesa_pd_env\Scripts
.\activate
pip install git+https://github.com/doesburg11/mesa_pd.git
cd C:\Users\peter\DataspellProjects\mesa_pd
mesa runserver predator_prey
```
Linux boot Botlzmann Wealth Model Network:
```bash
conda activate mesa_pd
pip install git+https://github.com/doesburg11/mesa_pd.git
cd /home/doesburg/DataspellProjects/mesa_pd/examples
#kill the server if occupied
kill -9 $(ps -A | grep python | awk '{print $1}')
mesa runserver boltzmann_wealth_model_network
```

Linux boot line by line:
```bash
conda activate mesa_pd
```
```bash
pip install git+https://github.com/doesburg11/mesa_pd.git
```
```bash
cd /home/doesburg/DataspellProjects/mesa_pd
```
```bash
#kill the server if occupied
kill -9 $(ps -A | grep python | awk '{print $1}')
```
```bash
mesa runserver predator_prey
```
