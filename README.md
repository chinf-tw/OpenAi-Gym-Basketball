# Reinforcement Learning Homework
This project is based on OpenAi Gym to create a basketball virtual environment with N.T.N.U. `jacky.baltes` homework [Reinforcement Learning - Assignment - Basketball](https://docs.google.com/document/u/1/d/e/2PACX-1vT0XRvEbnPDnAAlKCo1DP-8IFMccMgKfWaIBxO0n24CPDSE9PNfZOB10WS1zt9DlUPV8yEVzSOjgZmq/pub).
## Quick Start
### Download and Install
If you haven't git, you can just click the button `Clone or Download` and click `Download ZIP` to download this project.

If you have git, great! You can click the button `Clone or Download` copy the URL or just copy this `https://github.com/chinf-tw/OpenAi-Gym-Basketball` and go to your Terminal clone this project,like:
```bash
git clone https://github.com/chinf-tw/OpenAi-Gym-Basketball
```
### Start to Run
Go to the directory ,and using the Python3 to run `QLearningPolicy.py`, that will do add directory `v0-Qlearning-model` and using version `v0`,that command like:
```bash
cd OpenAi-Gym-Basketball
python3 QLearningPolicy.py
```
And you will see:
```
add the v0-Qlearning-model directory
choose the v0 version
Do you want to Render? 
```

You can input `1` to use the `Render` (not treaining), or `0` to run `Training` (not render).
## Parameter Setting
You can using the `python3 QLearningPolicy.py -h` or `python3 QLearningPolicy.py --help` to show this:
```
usage: QLearningPolicy.py [-h] [-d DIRECTORY] [-v VERSION] [-e EPSGREEDY]
                          [--end END]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Use the directory to place data model (default is
                        'v0-Qlearning-model')
  -v VERSION, --version VERSION
                        Choose the version to train model (now have
                        v0,v1,v2)(default is 'v0')
  -e EPSGREEDY, --epsGreedy EPSGREEDY
                        Give number of eps(default is 0.1)
  --end END             Expected number of operations, if number is -1 then
                        not end operations(default is -1)
```
If you want to use other not `v0-Qlearning-model` directory, you can use the optional arguments `-d` or `--directory` to create new directory or choose this directory to load training model.

If you want to use other not `v0` version, you can use the optional arguments `-v` or `--version` to create new training model or choose this training model.

### Example:
```bash
python3 QLearningPolicy.py -d v1-Qlearning-model -v v1 --end 1000
```
## Automatic Record Training Information
If use the `Training` (input `0`) then will automatic record training information with every `next 100 episode`.
### Record Mode
**File Type:** `csv`  
**File Naming Format:** `{vesion}_TrainingInfo.csv`
#### Record Type
- **Header:** `Episode`  
**Mean:** Numbers of episodes
- **Header:** `RewardSum`  
**Mean:** reward sum of `N` episodes divided by `N`
- **Header:** `isUseBadAction`  
**Mean:** numbers of bad action sum with `N` episodes(below numbers sum)
  - **Header:** `isGoOutSide`  
  **Mean:** numbers of robot leaves the playing field with `N` episodes divided by `N`
  - **Header:** `isOutSideShoot`  
  **Mean:** numbers of Euclidean distance between the robot and the basket > 4 with `N` episodes divided by `N`
  - **Header:** `isGoOutBall`  
  **Mean:** numbers of get the ball but leave the ball with `N` episodes divided by `N`

## References
1. Using Python cli tools `Argparse`
2. Using OpenAi gym `from gym.envs.classic_control import rendering`
3. Practical `jacky.baltes` homework [Reinforcement Learning - Assignment - Basketball](https://docs.google.com/document/u/1/d/e/2PACX-1vT0XRvEbnPDnAAlKCo1DP-8IFMccMgKfWaIBxO0n24CPDSE9PNfZOB10WS1zt9DlUPV8yEVzSOjgZmq/pub)