Select the @optimizer agent in Opencode.

Ask it to implement the system specified in the `AGENTS.md` file.

The optimizer will hand this off to the analyzer, who will spend a few minutes generating the code.

The optimizer will then call the profiler, who will verify that the code is fast enough on the small test data files. Most of the time, the profiler will also unpack stock.zip and then spend time profiling the code on that file. If you want to avoid that, move the file somewhere else for now.

If you want to see the loop in action, either ask it to process the full stock.zip file or reduce the SLA in AGENTS.md.

The optimizer agent file has instructions to stop looping after three iterations.
