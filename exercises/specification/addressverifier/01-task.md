This exercise is about making sure we and the LLM agree on what to build.

We'll use an apparently simple problem: a postal address verifier. Let's imagine we
want to build a function in python that takes a postal address and tells us if it's valid.

Prompt to the AI like this:

```
I want to create a tool for validating postal addresses.
```

Take a look at what the model does. Depending on model and context, the model may ask you questions, or it might just 
go straight to proposing a solution (or even writing code).

Let's narrow it down a bit:

```
We don't need to verify that the address exists, just that it is plausible. Everything the postal service would accept
as a delivery address should be accepted.

We'll pass the address to the code as a json object with fields such as **postcode** and **city**.
```

This, together with our AGENTS.md (which specifies we're using Python as well as a few general principles), will either get you 
more questions from the model or some code. Answer questions until you get some code, then take a look at the code and tests to
see what the AI has created.



