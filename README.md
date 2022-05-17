AI-program that generates policy for a given labyrinth

The labirynth has its edges as walls, an exit point that grants a reward to the agent and a hole that punishes the agent
The labirynth also has a STONE that serves as an obstacle
Agent's moves also have an element of randomness
Upon making a move there is chance that the agent will move in the wrong direction. The chance is represented with 'noise' and has to be accounted for by the agent.

The solution is so-called policy or a guide on how to act on any of the given cells
Each cell has a score and a direction, North, South, West or East.

All parts are customizable, the labyrinth size, number and locations of objects, rewards/punishments and noise

Example:

Initial state and the first iteration:  
![alt text](https://github.com/LuckyKot/Markov_Decision_Process/blob/c3c97981dc83a7567388f26b3630f46e75a7b6fe/example1.png)

15th iteration:  
![alt text](https://github.com/LuckyKot/Markov_Decision_Process/blob/c3c97981dc83a7567388f26b3630f46e75a7b6fe/example2.png)

Final, 30th iteration:  
![alt text](https://github.com/LuckyKot/Markov_Decision_Process/blob/c3c97981dc83a7567388f26b3630f46e75a7b6fe/example3.png)
We can clearly see the policy
