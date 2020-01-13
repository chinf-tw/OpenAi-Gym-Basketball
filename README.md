# Reinforcement Learning Homework
## Quick Start
### Download and Install
If you haven't git, you can just click the button `Clone or Download` and click `Download ZIP` to download this project.

If you have git, great! You can click the button `Clone or Download` copy the URL or just copy this `https://github.com/chinf1996/OpenAi-Gym-Basketball.git` and go to your Terminal clone this project,like:
```bash
git clone https://github.com/chinf1996/OpenAi-Gym-Basketball.git
```
### Start to run
Go to the directory ,and using the Python3 to run `QLearningPolicy.py`, that will do add directory `v0-Qlearning-model` and using version `v0`,that command like:
```bash
cd OpenAi-Gym-Basketball
python3 QLearningPolicy.py
```
And you will see the `add the v0-Qlearning-model directory`, `choose the v0 version`, and `Do you want to Render?`  
You can input `1` to see the training screen, or `2` to run high speed training (not training screen).
## Parameter setting
You can using the `python3 QLearningPolicy.py -h` or `python3 QLearningPolicy.py --help` to show this:
```
usage: QLearningPolicy.py [-h] [-d DIRECTORY] [-v VERSION]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        use the directory to place data model (default is
                        'v0-Qlearning-model')
  -v VERSION, --version VERSION
                        choose the version to train model (now have
                        v0,v1,v2)(default is 'v0')
```
If you want to use other not `v0-Qlearning-model` directory, you can use the optional arguments `-d` or `--directory` to create new directory or choose this directory to load training model.

If you want to use other not `v0` version, you can use the optional arguments `-v` or `--version` to create new training model or choose this training model.

example:
```bash
python3 QLearningPolicy.py -d v1-Qlearning-model -v v1
```