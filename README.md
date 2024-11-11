**Marijo1 is a 2-Player No-Limit Texas Hold'em Artificial Intelligence, which works with a regret minimization algorithm, that tries to compute the best possible action distribution for any action to do.**

**The AI works with the following constraint: when making a prediction, it cannot compute any possible response from the opponent, or any other action to do later in the game.**

Why? Because the game of Poker is already solved (with CFR, CFR+, Linear CFR, Deep-CFR, ...) and this AI was made firstly to have fun, and secondly to be extremly fast.

Marijo1 is not super-human, and is beatable, if you are a good player and are focused, but it plays well, with great speed.

**You can find the full code of the AI in the ai/ folder. You can play against the ai with the code in the lab/ folder:**

You can play a full game against Marijo1 with lab/user_vs_ai.py, or hand by hand (with chips reset after each game, and the total return of the AI in memory) with lab/user_vs_ai_handsOnly.py.

In both scripts, you can customize your playing experience. Among other things, you can use the **print_ai_cards** variable, set to True or False, to print the cards of Marijo1 in the terminal.

You can also use the **ai_verbose_level** variable to print different informations in the terminal:

A verbose level of 1 will print the action distribution of the AI (the result of the AI computation, before making a move).

A verbose level of 2 will print the above, and the number of iterations of the AI (the number of games simulated).

A verbose level of 3 will print the above, and the raw regrets, before computing the action distribution.

A verbose level of 4 will print the above, and (coupled with the value of verbose_iteration_steps) will print the cards of (some of) the simulations of the game when computing the regrets.
