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
