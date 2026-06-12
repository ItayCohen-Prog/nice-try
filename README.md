Nice Try
========

Work in progress.

Nice Try is a learning project for building a CLI that runs agent attempts in
clean, repeatable loops. The basic idea is to avoid accumulative errors by
saving what was learned from each attempt, resetting the working area, and
trying again from a clean base.

Core idea:

- Create a better `/goal`-style loop where an agent keeps working until a goal is
  achieved.
- Store each attempt's result, summary, and useful learnings.
- Reset the working area between attempts so old failed work does not pollute
  the next run.
- Use the saved learnings to improve the next attempt.

Future feature: find the one-shot prompt
----------------------------------------

Aside from the basic Nice Try retry-loop functionality, I want the tool to help
answer this question:

Can this type of task be one-shot?

The tool should eventually synthesize the lessons from repeated attempts into a
single prompt that can recreate the desired result from scratch. After finding
that candidate one-shot prompt, it should run it several more times against the
same validation test and report how reliable it was, for example `7/10` passed.
I can then add further looping where the agent will keep adjusting the prompt until 
he managed to cross a certain percentage of success like 7/10 or 5/10. 
this opens the doors to creating something along the lines of a One Shot This Bench 
where the model is tested no its ability to make a one shot prompt to pass a certain text 
which I think is really cool. 
