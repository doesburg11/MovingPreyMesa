Install Mesa:
<a name="install">Install Mesa</a>
```bash
conda activate mesa_pd
pip install git+https://github.com/doesburg11/mesa_pd.git
cd /home/doesburg/DataspellProjects/mesa_pd
#kill the server if occupied
kill -9 $(ps -A | grep python | awk '{print $1}')
mesa runserver examples/wolf_sheep
```

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
mesa runserver examples/wolf_sheep
```

The scheduler first outputs all Predators reshuffled and then all Prey reshuffled.
Not all agents reshuffled together that is.
 This is probably initiated by:
/home/doesburg/DataspellProjects/mesa_pd/mesa/time.py
and step_type() and step()

To do:
Top bar color: #0C3C60
