# Reinforcement Learning - Assignment - Basketball - Evaluation
## Use QTables Motivation
To reach my goal faster, I used `three QTables`, these tables are used:
1. **Variable name:** `qlearningBall`  
**mean:** Using this QTable before agent get the ball.
2. **Variable name:** `qlearningShoot`  
**mean:** Using this Qtable when agent get the ball and shoot the ball (if do not successful to shoot and do not have the ball).
3. **Variable name:** `qlearningGetBall`  
**mean:** Using this QTable when agent get the ball.

## Extra Design
- The episode will end if agent got the ball but it leave the ball (using action `Movement` when got the ball )

## Tring Training
### Try to train 10000 episodes (epsGreedy = 0.1)
![training 10000 Episode](img/training&#32;10000&#32;Episode.svg)  
We can saw that,`isGoOutSide` was obvious convergence near 1000 episodes,and `isOutSideShoot` was better with after 6000 episodes but that wasn't obvious.  

I guess `isGoOutSide` wasn't convergence to 0 because epsGreedy,so I tried to use `epsGreedy = 0.1` with 2000 episodes,and tried to use `epsGreedy = 0` after 2000 episodes,and retraining 2000 episodes.
  
  
![training 4000 Episode](img/training&#32;4000&#32;Episode.svg)
We can saw that the agent leaved the playing field 8 in last 100 episodes,this result was not bad,but that didn't best result,so I tried to retraining 1000 episodes with `epsGreedy = 0` to see if there will be better results.

![training 5000 Episode](img/training&#32;5000&#32;Episode.svg)

I saw this figure,I thought about WTF... what went wrong?  
So I tried to render that, I saw...  
![wrong](img/wrong.gif)

Finally, I retrained 5000 episodes with `epsGreedy = 0.1`, finally rendering was:
![finally](https://media.giphy.com/media/fY5QI1PuF7z8gLiL0a/giphy.gif)