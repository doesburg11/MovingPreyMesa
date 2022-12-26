### Install Mesa:

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
