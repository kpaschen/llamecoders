Now that we've got some basic coding experience, let's ask the LLM to create a *Sudoku solver* for us.

As before, we present Sudoku puzzles to the LLM as text files. However, now we represent _empty_ squares with zeroes.

We want the LLM to write code that takes a Sudoku puzzle and returns a solution.

For example, when we present the input

```
5,3,0,0,7,0,0,0,0
6,0,0,1,9,5,0,0,0
0,9,8,0,0,0,0,6,0
8,0,0,0,6,0,0,0,3
4,0,0,8,0,3,0,0,1
7,0,0,0,2,0,0,0,6
0,6,0,0,0,0,2,8,0
0,0,0,4,1,9,0,0,5
0,0,0,0,8,0,0,7,9
```

we want to get the output

```
5,3,4,6,7,8,9,1,2
6,7,2,1,9,5,3,4,8
1,9,8,3,4,2,5,6,7
8,5,9,7,6,1,4,2,3
4,2,6,8,5,3,7,9,1
7,1,3,9,2,4,8,5,6
9,6,1,5,3,7,2,8,4
2,8,7,4,1,9,6,3,5
3,4,5,2,8,6,1,7,9
```

Prompt the LLM, get it to generate the code and tests. Run the tests and try the code.

Does the code work?

Do the tests make sense?

What does the code do when there is more than one solution?

What does the code do when there is no solution?
