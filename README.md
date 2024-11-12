**Marijo1 is a 2-Player No-Limit Texas Hold'em Artificial Intelligence, which works with a regret minimization algorithm, that tries to compute the best possible strategy for any situation it is in.**

**The AI works with the following constraint: when making a prediction, it cannot compute any possible response from the opponent.**

Why? Because the game of Poker is already solved (with CFR, CFR+, Linear CFR, Deep-CFR, ...) and this AI was made to have fun, and be extremely fast.

Marijo1 is clearly not super-human, but it is strong enough, for example, to be integrated into a Poker application.

**You can play against the AI with the script user_vs_ai.py, present in the lab/ folder.**

In it, you can customize your playing experience. Among other things, you can use the **print_ai_cards** variable, set to True or False, to print the cards of Marijo1 in the terminal.

You can also use the **ai_verbose_level** variable to print different informations in the terminal:

A verbose level of 1 will print the strategy of the AI (the result of the algorithm).

Verbose levels superior to that print more and more information, related to that computation.

Please note than when you want to raise, you need to include the amount needed to match the bet of the AI (if the AI bets 20, you need to bet 50 to make a raise of 30).

**Finally**, on top of Python 3 and its standard library, you will need to have Treys (pip install treys) and Numpy (pip install numpy) on your machine to use Marijo1.
