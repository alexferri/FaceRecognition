/*
 * Author: Alexandre Ferri
 * Created on Mon Dec 09 2019
 */

## Initialize this project

```dependencies
https://github.com/PyMySQL/mysqlclient-python >>> if needed only

** install MINICONDA **
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

```

```setup this project

1 -> conda create -n FaceRecognition python=3.7
2 -> conda init zsh
3 -> close and open the terminal
4 -> conda activate FaceRecognition

5 -> run sh commands bellow.
```

```sh
pip install -r requirements.txt

export FLASK_APP=source
export FLASK_ENV=Development
export FLASK_DEBUG=True
```

```Commands
* Runing server => python server.py
* Runing server dev => flask run --host=0.0.0.0
* View active routes => flask routes
* List of conda enviroments => conda env list
```
