# Style

Use this reference for the user's personal coding preferences. For non-Python code, apply the general parts that make sense and ignore Python-only details.

## Principles

- Prefer readable, clean, locally understandable code.
- Do not optimize for mechanical rule coverage.
- Keep simple code simple; do not add ceremony just to look formal.
- Follow strong project-local conventions when they conflict with this reference.
- Assume callers follow type annotations by default; do not add runtime type checks or defensive branches unless they protect a real boundary or failure mode.
- Use Ruff for Python formatting and basic linting; use this file for judgment Ruff cannot infer.

## Documentation

- Document code only when the intent, responsibility, or workflow is not obvious from the code itself.
- Classes should usually have docstrings because they define state, responsibilities, and interaction boundaries.
- Core entry functions should have docstrings when they represent a larger workflow or feature surface.
- Simple functions with obvious behavior can rely on type annotations only.
- For Python library code, use concise NumPy-style docstrings and raw docstrings: `r"""..."""`.
- For complex classes, add a `Workflow` section with top-to-bottom numbered steps.
- Do not require module docstrings.

Example:

```python
class Trainer:
    r"""Train and evaluate a model.

    Parameters
    ----------
    model : nn.Module
        Model to optimize.

    Workflow
    --------
    1. prepare a batch.
    2. compute outputs and loss.
    3. update parameters.
    4. collect metrics.
    """
```

## Comments

- Write inline comments rarely.
- Add comments for intent, constraints, algorithmic steps, shape changes, or non-obvious reasons.
- Do not restate what is already implied by the code.
- Start inline comments with lowercase text.
- Avoid section separator comments; prefer real structure and semantic blank lines.

## Types

- Type annotations should improve readability and cleanliness, not satisfy type checking at all costs.
- Trust type annotations in internal code by default.
- Public Python functions and methods should annotate parameters and return values.
- Complex private helpers should also be annotated.
- Simple local variables do not need annotations.
- Use `Any` when precise typing would make code noisy.
- In Python, prefer `Optional[T]`, `List[T]`, `Dict[K, V]`, and `Tuple[...]`.
- Avoid extra runtime type checks or validation branches unless input crosses a real boundary, such as user input, files, network data, CLI arguments, or third-party APIs.

## Naming

- Default to `snake_case` for public APIs, method names, arguments, and attributes.
- Local variables can be short when nearby context makes them clear.
- Prefer full words for short natural-language words.
- For longer words (more than roughly 7 characters), use common abbreviations when they stay readable.
- In math, model, tensor, and pipeline code, short names such as `x`, `y`, `z`, `q`, `k`, and `v` are acceptable.
- Short dimension names such as `B`, `S`, `D`, `H`, `N`, and `C` are acceptable in tensor code.
- Follow existing project-local special naming, including mixed-case local tensor variables, but keep `snake_case` as the default.

## Code Shape

- Do not impose a hard function length limit.
- Keep logically complete code together when that improves reading continuity.
- Prefer compact expressions when they remain easy to read.
- Split important intermediate values when they carry meaning or help debugging.
- Extract helpers conservatively: repeated logic, independent concepts, or clear complexity reduction only.
- Avoid scattering the main reading path across many small helpers.

Example:

```python
scores = (queries @ keys.transpose(-2, -1)) / dim**0.5
weights = scores.masked_fill(mask == 0, float("-inf")).softmax(dim=-1)
outputs = weights @ values
```

## Interfaces and Layout

- Public Python library modules should define `__all__`.
- Scripts and tests do not need `__all__`.
- Package `__init__.py` files should re-export common public APIs and define matching `__all__`.
- Use this Python file layout for library modules: imports, `__all__`, constants, classes/functions.
- Order class methods by usage logic and dependency flow, keeping related methods near each other.
- In `__init__`, assign attributes by importance first, then semantic grouping.
- Use semantic blank lines inside functions, such as between initialization, main work, and return.

## Signatures and Calls

- When a long signature wraps, do not force one parameter per line.
- Keep semantically related parameters on the same line when readable.
- In multi-line calls, prefer explicit keyword arguments when that improves readability.

Examples:

```python
def build_model(
    num_users: int, num_items: int,
    embedding_dim: int, dropout_rate: float = 0.1,
) -> nn.Module:
    ...


trainer = Trainer(
    model=model, optimizer=optimizer,
    train_loader=train_loader, valid_loader=valid_loader,
    epochs=100, device="cuda",
)
```

## Tests and Scripts

- Tests should prioritize clarity over abstraction.
- Small amounts of repetition in tests are acceptable.
