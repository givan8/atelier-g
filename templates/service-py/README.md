# {{PROJECT_NAME}}

<!-- One sentence: what this does and who it is for. Replace the TODOs below with
     what is actually true. A README that says TODO on day one says TODO forever. -->

TODO — what this service does.

Built from the `{{TEMPLATE}}` template of
[atelier-g](https://github.com/givan8/atelier-g). Agents working here should read
[`AGENTS.md`](AGENTS.md) first.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
python -m app
curl localhost:8080/health
```

## Test

```bash
pytest              # tests
ruff check .        # lint
mypy                # types
pytest && ruff check . && mypy    # the same checks CI runs
```

## Layout

```
src/app/        application code
src/app/__main__.py   entry point (python -m app)
tests/          tests, mirroring src/app
docs/adr/       decisions — read these before changing the design
```

## Configuration

All configuration comes from the environment. [`.env.example`](.env.example) lists
every variable the service reads. No secrets in the repository, ever.

## Deploy

TODO — how this is deployed, and how to roll it back.
