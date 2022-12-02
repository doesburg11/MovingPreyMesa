Install Mesa:

```bash
conda activate mesa_pd
pip install git+https://github.com/doesburg11/mesa_pd.git
cd /home/doesburg/DataspellProjects/mesa_pd
#kill the server if occupied
kill -9 $(ps -A | grep python | awk '{print $1}')
mesa runserver examples/wolf_sheep
```
