**Marijo1 is a 2-Player No-Limit Texas Hold'em Artificial Intelligence, which works with a regret minimization algorithm, that tries to compute the best possible strategy for any situation it is in.**

The AI works with the two following constraints: 

- When making a prediction, it cannot compute any possible response from the opponent.

- No strategy about Poker (for example what to do at each round, with each hand) can be put into the algorithm. The only thing allowed is to know wether the AI engages the action or not.

Why? Because the game of Poker is already solved (with CFR, CFR+, Linear CFR, Deep-CFR, ...) and this AI was made to have fun, and be extremely fast.

Therefore, Marijo1 is not super-human, but it plays very well, with astonishing speed.

**You can play against the AI with the script 'user_vs_ai.py', present in the 'lab' folder.**

When starting,the script will ask you if you want to print the cards of Marijo1 in your terminal, and the verbose level you desire while playing.

A verbose level of 0 won't output any information not needed to play.

A verbose level of 1 will print the strategy of the AI (the result of the algorithm).

Verbose levels superior to that will output more and more information, related to the computation of the algorithm.

Please note than when you want to raise, you need to include the amount needed to match the bet of the AI (if Marijo1 bets 20, you need to place 50 on the table to make a raise of 30).

**Finally**, on top of Python 3 and its standard library, you will need to have Treys (pip install treys) and Numpy (pip install numpy) on your machine to use Marijo1.

Enjoy, and feel free to try to improve the algorithm!
