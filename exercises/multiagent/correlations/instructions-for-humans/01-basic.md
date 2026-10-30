Select the @optimizer agent in Opencode.

Ask it to implement the system specified in the `AGENTS.md` file.

The optimizer will hand this off to the analyzer, who will spend a few minutes generating the code.

The optimizer will then call the profiler, who will verify that the code is fast enough on the small test data files.

You can unzip stock.zip to get another larger test data file if you want the performance analysis to be more thorough.
Depending on your computer, this may or may not cause the profiler to diagnose the program as too slow.
