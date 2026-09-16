---
name: experiment
description: Set up a new experiment the reproducible way - state the hypothesis, copy the baseline config into a new dated file, smoke-run on a tiny subset, and record the run in the experiment log. Use when asked to try a new idea, tune a hyperparameter, compare against a baseline, or "run an experiment".
---

# New Experiment Procedure

Never edit a baseline config or launch a full run ad hoc. Follow this order:

## Step 1: Hypothesis
- Write one sentence: *"If I change X, metric Y will move because Z."*
- Name the baseline run this will be compared against (config path + result
  directory). If there is no baseline, say so — the first run **is** the
  baseline.

## Step 2: Config
- Copy the baseline config to `configs/<YYYYMMDD>_<short_name>.yaml`.
- Change **only** the knobs the hypothesis needs. Diffing the two configs must
  fully explain the experiment.
- Set `seed` explicitly. Set the output directory to `outputs/<YYYYMMDD>_<short_name>/`.
- Do NOT touch the baseline config file.

## Step 3: Smoke Run
- Run `uv run python -m src.train --config configs/<new>.yaml --debug`
  (tiny subset, CPU or a single GPU step). This validates the code path,
  config keys, and shapes without spending GPU hours.
- Fix any failure here before proceeding. If the smoke run cannot be executed
  in this environment, state it explicitly.

## Step 4: Full Run (only with explicit user request)
- Do NOT start a full training run on your own. Present the exact command and
  let the user launch it:
  ```sh
  uv run python -m src.train --config configs/<new>.yaml
  ```

## Step 5: Log Entry
- Append one row to `experiments/LOG.md` (create it if missing):

  | date | run name | hypothesis | config | seed | git hash | key metric (baseline → result) | status |
  | --- | --- | --- | --- | --- | --- | --- | --- |

- Status is `smoke-ok`, `running`, `done`, or `failed`. Fill the metric
  column only with numbers read from `outputs/<run>/metrics.*` — never from
  memory or estimation.

## Step 6: Handoff
- Finish with `.claude/HANDOFF.md` per `.claude/rules/handoff.md`, including
  the 🧪 실험 정보 section (config, seed, git hash, result path, metric delta).
