The exercises in this directory are about multiple agents interacting.

Make sure your opencode can see the sample agents `optimizer`, `analyst` and `profiler` (use `/agents` to list them).

Copy the file `WORKFLOW_STATE_TEMPLATE.md` to `WORKFLOW_STATE.md`.

This is a demo for how multiple agents can interact. We have two agents performing different aspects of the work, and a third one is managing them:

1. The `analyst` agent writes code that meets the functional specification
2. The `profiler` agent checks the code for performance issues
3. The `optimizer` agent calls the analyzer and the profiler, looping if necessary.

The analyst and profiler use `WORKFLOW_STATE.md` as a scratchpad where they can exchange information.

This is a very basic orchestration; other options exist.
