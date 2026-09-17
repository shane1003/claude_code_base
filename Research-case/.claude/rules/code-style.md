# Python & ML Research Style Guide

This document outlines the coding standards, formatting guidelines, and research-code practices for Python / PyTorch experiment repositories. All code must comply with these guidelines.

---

## 1. Code Formatting & Linting
- **Formatter & Linter**: Code formatting and linting are enforced by `ruff`.
- **Line Length**: Maximum line length is **88 characters** (Black/ruff default; intentionally wider than PEP 8's 79).
- **Indentation**: Use 4 spaces per indentation level. No tabs.
- **Encoding**: UTF-8 source file encoding.
- **Notebooks**: Outputs are stripped before commit (`nbstripout`, enforced by hook). Notebooks are for exploration only and are never imported.
- **Markdown is excluded from ruff**: since ruff 0.14, `ruff format` also rewrites Python code blocks inside `.md` files. `ruff.toml` excludes them so that documentation, including this file, is never silently reformatted. The Python examples below are therefore hand-maintained: keep them formatted correctly by hand.
- **Artifact directories are excluded from ruff**: `outputs/`, `data/`, `weights/`, `runs/`, and `checkpoints/` are listed in `ruff.toml` so no tool rewrites a finished run.

---

## 2. Naming Conventions
Follow standard PEP 8 naming conventions (PEP 8 §Naming Conventions):

| Category | Convention | Example |
| :--- | :--- | :--- |
| **Modules / Files** | `snake_case` | `coco_dataset.py` |
| **Classes** | `PascalCase` | `TrackingDataset` |
| **Functions / Methods** | `snake_case` | `compute_auc()` |
| **Variables** | `snake_case` | `batch_size` |
| **Constants** | `UPPER_SNAKE_CASE` | `IMAGENET_MEAN` |
| **Type Variables / Generics** | `CapWords`, short; `_co`/`_contra` suffix for variance | `T`, `BatchT` |
| **Exceptions** | `PascalCase` ending in `Error` | `CheckpointNotFoundError` |
| **Packages (directories)** | lowercase, no underscores if possible | `data`, `models`, `eval` |
| **Internal / private names** | single leading underscore | `_collate()`, `_cache` |
| **Config files** | `<YYYYMMDD>_<short_name>.yaml` | `20260916_resnet50_lr1e-3.yaml` |
| **Run directories** | `<YYYYMMDD>_<short_name>/` | `outputs/20260916_resnet50_lr1e-3/` |

---

## 3. Type Annotations & Safety
- **Explicit Types**: All function signatures (arguments and return types) **must** have explicit type hints.
- **Modern Syntax (Python 3.10+)**: Use built-in type generics and standard union syntax:
  - Good: `list[str]`, `dict[str, Any]`, `str | None`
  - Avoid: `List[str]`, `Dict[str, Any]`, `Optional[str]`
- **Tensors**: Annotate as `torch.Tensor` / `np.ndarray` and document the **shape and dtype** in the docstring or an inline comment, e.g. `# (B, C, H, W) float32`. Shape bugs are the most common silent failure in research code.
- **Avoid `Any`**: Minimize the use of `typing.Any`. Define `TypedDict`, `dataclass`, or `Protocol` for config and batch structures.

---

## 4. Documentation (Google Docstring Format)
All public functions, classes, and scripts must include Google-style docstrings
(Google Python Style Guide §3.8). Summary line is descriptive ("Computes ..."), one line,
ending with a period. Section headers: `Args:`, `Returns:`, `Yields:` (generators),
`Raises:`, `Attributes:` (classes). For tensor arguments, state shape and dtype.

```python
def compute_auc(scores: torch.Tensor, labels: torch.Tensor) -> float:
    """Computes ROC-AUC for binary predictions.

    Args:
        scores: Predicted scores, shape (N,), float32. Higher means positive.
        labels: Ground-truth labels, shape (N,), int64 in {0, 1}.

    Returns:
        Area under the ROC curve in [0.0, 1.0].

    Raises:
        ValueError: If shapes differ or labels contain only one class.
    """
    if scores.shape != labels.shape:
        raise ValueError(f"Shape mismatch: {scores.shape} vs {labels.shape}")
    if labels.unique().numel() < 2:
        raise ValueError("AUC is undefined when only one class is present.")
    ...
```

Class docstrings describe the object and list public attributes:

```python
class TrackingDataset(Dataset):
    """Frame-pair dataset for object tracking.

    Attributes:
        root: Directory containing sequence folders.
        seq_len: Number of consecutive frames returned per sample.
        transform: Callable applied to each frame tensor (C, H, W).
    """

    def __init__(self, root: Path, seq_len: int = 2, transform: Callable | None = None) -> None:
        self.root = root
        self.seq_len = seq_len
        self.transform = transform
```

---

## 5. Research Code Conventions
### 5.1 Reproducibility
- A single `set_seed(seed: int)` in `src/utils` seeds `random`, `numpy`, `torch` (CPU + CUDA) and sets `torch.backends.cudnn.deterministic`. Call it once at entry.
- Every run records: resolved config, seed, git commit hash, data version, and package versions. Write them to the run directory before training starts.
- Nondeterministic ops (e.g. `torch.use_deterministic_algorithms(False)`) must be documented in the config with a reason.

### 5.2 Config-Driven Experiments
- No magic numbers in `src/`. Learning rate, batch size, thresholds, paths, and augmentation parameters all come from the config.
- Load config into a typed structure (`dataclass` / `TypedDict`) once, at the entry point. Pass it down explicitly; never read config from a global.
- A new experiment = a new config file. Diffing two configs must fully explain the difference between two runs.

### 5.3 Device & Resource Handling
- Resolve device once (`src/utils.get_device(cfg)`) and pass it explicitly. Never `torch.device("cuda:0")` inline.
- Move data to device inside the training loop, not in the dataset (keeps workers CPU-only and picklable).
- Use `torch.no_grad()` / `torch.inference_mode()` for evaluation. Free large tensors (`del`, `torch.cuda.empty_cache()`) only when profiling shows a need.

### 5.4 Metrics & Evaluation
- Metric functions are **pure**: tensors in, numbers out, no I/O, no global state.
- Every metric has a known-answer test in `tests/` (hand-computed small example). Changing a metric without changing its test is a review blocker.
- Evaluation scripts never modify weights or data. They read a checkpoint and write a metrics file.

### 5.5 Logging
- Use `logging` (or the project's experiment tracker), never bare `print()` in `src/`.
- Log at epoch/step boundaries: loss, metrics, lr, throughput. Log the full resolved config once at startup.

---

## 6. Error Handling
- **Fail loudly on missing inputs**: a missing data file, checkpoint, or config key raises immediately with a clear message. Never fall back to random init, an empty dataset, or a default path silently.
- **Assert shapes at boundaries**: check tensor shapes/dtypes at module and dataset boundaries with explicit error messages. Silent broadcasting is the enemy.
- Never use bare `except:` statements. Always catch specific exceptions (`except FileNotFoundError as exc:`).

```python
# Good: explicit, loud failure
ckpt_path = Path(cfg.eval.ckpt)
if not ckpt_path.is_file():
    raise CheckpointNotFoundError(f"Checkpoint not found: {ckpt_path}")
state = torch.load(ckpt_path, map_location=device)
```

---

## 7. Import Ordering
Imports should be grouped logically and sorted alphabetically within each group using ruff (isort rules):

1. Standard library imports
2. Third-party library imports (torch, numpy, etc.)
3. Local application imports (src.data, src.models, etc.)

```python
import logging
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from src.data.tracking_dataset import TrackingDataset
from src.utils.seed import set_seed
```
