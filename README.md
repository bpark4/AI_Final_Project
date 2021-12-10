Final Project for Introduction to AI, Fall 2021

Project Name: Comparison of Search Based algorithms and Reinforcement Learning algorithms in 
the game of snake.

Program Files:

snake_bfsearch.py --> Run with "python snake_bfsearch.py". Will run 10 playthroughs using
			breadth first search as the search algorithm.

snake_astarsearch.py --> Run with "python snake_astarsearch.py". Will run 10 playthroughs using
			A* search as the search algorithm.

snake_rl.py --> Run with "python snake_rl.py". By default will train for 1000 trials with
			default epsilon=0.5, default alpha=0.2, default discount=1, then will
			run 10 playthroughs using the trained Q-Values as a policy.

		To change number of trials, epsilon, alpha, or discount go to Trainer class
			__init__ and change the values of the __init__ parameters

		To change living reward, go to Trainer class function "def update" and change
			the line 589 to desired living reward

Results Files:

BF_Results.txt --> Results of a block of playthroughs for breadth first search, including
			mean score, mean apples, mean time, and mean score per second 

AStar_Results.txt --> Results of a block of playthroughs for A* search, including
			mean score, mean apples, mean time, and mean score per second 

RL_Results.txt --> Results of blocks of playthroughs, varying parameters (alpha,discount,trials,
			living reward), including mean score, mean apples, mean time, number of
			loops, and mean score per second.

Comparison Files:

Comparison.txt --> Gives a comparison of A*, breadth first, and RL algorithms, choosing a
			winner of which algorithm is best for the game of snake.

Presentation Files:

project_proposal_AI.pptx --> Initial Proposal Presentation

snake_algorithms.pptx --> Final presentation included in youtube video

Additional Files:

apple.png --> Picture for the apple

pygame.png --> Picture for the snake pieces

