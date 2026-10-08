# Interview practice set

Coding-interview practice problems grouped by pattern, with LeetCode links and a
progress tracker that saves in your browser. To carry progress to another
device use "Copy progress link" (the solved set is encoded in the URL fragment)
or export/import a small JSON file; imports merge, they never remove ticks.

Live page: https://pankajkgarg.github.io/interview-practice/

The sections follow the chapters of the *Coding Interview Refresher* book and the
explainer video. Each section opens with the recognition cue for its pattern.
Problems come from [NeetCode 150](https://neetcode.io/practice) (all 150),
[Grind 75](https://www.techinterviewhandbook.org/grind75/) (all 75) and the book's
own picks; the tags on each row say which.

Files:

- `index.html`: the page, self-contained.
- `problems.json`: the same data, for other tools.
- `problems.py` + `build.py`: edit the Python list and run `python3 build.py` to regenerate both.

## Eval study notes

`eval/` holds study notes on LLM evaluation (statistics and platform engineering),
live at https://pankajkgarg.github.io/interview-practice/eval/. The pages are built
from the *Evaluation Field Guide* chapters with `python3 eval/build_eval.py <chapters-dir>`
(needs pandoc). Hand-written pages are in `eval/src/`, and each video's single
context file (narration plus on-screen notes) is in `eval/videos/`.
