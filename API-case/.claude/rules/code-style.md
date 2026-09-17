# Python & FastAPI Style Guide

This document outlines the coding standards, formatting guidelines, and architectural practices for Python and FastAPI projects. All code must comply with these guidelines.

---

## 1. Code Formatting & Linting
- **Formatter & Linter**: Code formatting and linting are enforced by `ruff`.
- **Line Length**: Maximum line length is **88 characters** (Black/ruff default; intentionally wider than PEP 8's 79).
- **Indentation**: Use 4 spaces per indentation level. No tabs.
- **Encoding**: UTF-8 source file encoding.
- **Markdown is excluded from ruff**: since ruff 0.16.0, `ruff format` also rewrites Python code blocks inside `.md` files. `ruff.toml` excludes them so that documentation, including this file, is never silently reformatted. The Python examples below are therefore hand-maintained: keep them formatted correctly by hand.

---

## 2. Naming Conventions
Follow standard PEP 8 naming conventions (PEP 8 §Naming Conventions):

| Category | Convention | Example |
| :--- | :--- | :--- |
| **Modules / Files** | `snake_case` | `user_service.py` |
| **Classes** | `PascalCase` | `UserRepository` |
| **Functions / Methods** | `snake_case` | `get_user_by_id()` |
| **Variables** | `snake_case` | `current_user` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| **Type Variables / Generics** | `CapWords`, short; `_co`/`_contra` suffix for variance | `T`, `UserT`, `KeyT_co` |
| **Exceptions** | `PascalCase` ending in `Error` | `UserNotFoundError` |
| **Packages (directories)** | lowercase, no underscores if possible | `services`, `core` |
| **Internal / private names** | single leading underscore | `_build_query()`, `_cache` |

---

## 3. Type Annotations & Safety
- **Explicit Types**: All function signatures (arguments and return types) **must** have explicit type hints.
- **Modern Syntax (Python 3.10+)**: Use built-in type generics and standard union syntax:
  - Good: `list[str]`, `dict[str, Any]`, `str | None`
  - Avoid: `List[str]`, `Dict[str, Any]`, `Optional[str]`
- **Avoid `Any`**: Minimize the use of `typing.Any`. Define `TypeVar`, `Protocol`, or `Pydantic` schemas where applicable.

---

## 4. Documentation (Google Docstring Format)
All public functions, classes, and API route handlers must include Google-style docstrings
(Google Python Style Guide §3.8). Summary line is descriptive ("Calculates ..."), one line,
ending with a period. Section headers: `Args:`, `Returns:`, `Yields:` (generators),
`Raises:`, `Attributes:` (classes).

```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculates the discounted price for a given product.

    Args:
        price: The original price of the product (must be > 0).
        discount_rate: Discount percentage between 0.0 and 1.0.

    Returns:
        The final price after applying the discount.

    Raises:
        ValueError: If price or discount_rate is out of valid bounds.
    """
    if price <= 0 or not (0 <= discount_rate <= 1):
        raise ValueError("Invalid price or discount rate.")
    return price * (1 - discount_rate)
```

Class docstrings describe the object and list public attributes:

```python
class UserRepository:
    """Data-access layer for User entities.

    Attributes:
        session: The database session used for all queries.
        default_page_size: Number of rows returned when no limit is given.
    """

    def __init__(self, session: Session, default_page_size: int = 50) -> None:
        self.session = session
        self.default_page_size = default_page_size
```

---

## 5. FastAPI Architecture Conventions
### 5.1 Schema vs. Model Separation
- Schemas (app/schemas/): Pydantic v2 models strictly used for request parsing and response serialization (DTOs).
- Models (app/models/): Database ORM entities (SQLAlchemy, SQLModel).
- Rule: Never leak DB ORM models directly into API responses. Always convert to Pydantic schemas.

### 5.2 Dependency Injection
- Use FastAPI's Depends() for injecting database sessions, authentication contexts, and shared business logic.
- Avoid global mutable instances or inline instantiation within route functions.

```Python
@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)
```

### 5.3 Async Usage
- async def: Use for I/O-bound operations (DB queries, external HTTP calls).
- def: Use for pure CPU-bound computations or sync utility functions.

## 6. Error Handling
- Use structured exceptions. Raise domain-specific exceptions in service layers and map them to HTTP responses via global error handlers or standard HTTPException.
- Never use bare except: statements. Always catch specific exceptions (except ValueError as e:).
```Python
# Good Exception Handling
try:
    user = service.get_user(user_id)
except UserNotFoundError as exc:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {user_id} not found."
    ) from exc
```

## 7. Import Ordering
Imports should be grouped logically and sorted alphabetically within each group using ruff (isort rules):

1. Standard library imports
2. Third-party library imports (FastAPI, Pydantic, SQLAlchemy, etc.)
3. Local application imports (app.core, app.services, etc.)

```Python
import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.services.user_service import UserService
```