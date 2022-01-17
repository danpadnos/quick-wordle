# Quick Wordle Solver

Inspired by [wordle-hacker](https://github.com/idofrizler/wordle-hacker) and uses the same method, essentially. Faster implementation using a lot of precomputation / memoization. 

To benchmark on all 2315 [wordle](https://www.powerlanguage.co.uk/wordle/) puzzle words run:

```
python wordle_solver.py
```

Sample output:

```
calculating guess2pattern2secrets.... 
done in 118.83 seconds
starting benchmark on 2315 puzzle words...
done in 200.21 seconds
====================
total games: 2315
successful games: 2315
average turns in successful games: 3.65
```

The run time above (around 5 minutes 20 seconds) was measured on a 2018 MacBook Pro with a 2.3 GHz Quad-Core Intel Core i5 processor.