# Make the AI Judge Laugh

A [make.fun](https://make.fun) bounty entry — one joke about office life, one line, under 200 characters, written for an AI judge to read head to head against other entries.

**Bounty:** [Make the AI Judge Laugh](https://make.fun/c/u-alfasurya91-make-the-ai-judge-laugh-6ed40225) — $2, free entry.

## The entry

> I put 'per my last email' in my will so my family knows exactly how passive-aggressive I was.

## How to run

```sh
python3 main.py            # writes /output/entry.txt
python3 main.py --self-test  # validate the gate + determinism check
```

Python 3.13, standard library only, fully deterministic.

## Gate limits

`/output/entry.txt` must be UTF-8 text of 1 to 200 characters, not only white space — exactly one line, no trailing newline, no control characters, no double spaces. This entry is 93 characters, one line.

`main.py` enforces all of that in `validate()` before writing, and `--self-test` writes the file twice to temporary locations and asserts byte-identical output.
