This exercise is a first tour around agentic coding.

We'll start from a simple problem: A Sudoku solution verifier.

Sudoku are a number-placement puzzle played on a 9x9 grid. [Wikipedia](https://en.wikipedia.org/wiki/Sudoku/)

We want to build a function in Python that takes a Sudoku solution and decides whether it satisfies the rules.

Prompt the AI like this:

```
I want to create a tool for validating Sudoku solutions.
```

Take a look at what the model does. Depending on model and context, the model may ask you questions, or it might just 
go straight to proposing a solution (or even writing code).

Let's narrow it down a bit:

```
Solutions should be presented as text files with nine lines of nine numbers each.
The program should take one such file, process it, and return "True" if the solution is valid, and "False" if it isn't.
```

This, together with our AGENTS.md (which specifies we're using Python as well as a few general principles), will either get you 
more questions from the model or some code. Answer questions until you get some code, then take a look at the code and tests to
see what the AI has created.

