# Contributing

This repository is a published copy of the VAIF Studio Python SDK. VAIF Studio
maintains the SDK in its own source tree and publishes it here.

## Reporting bugs and requesting features

Bug reports and feature requests are welcome as
[GitHub issues](https://github.com/vaifstudio/vaif-python/issues). For a bug,
include:

- the package version (`python -c "import vaifstudio; print(vaifstudio.__version__)"`),
  your Python version and your operating system;
- a minimal code sample that reproduces the problem;
- the full exception, including `status`, `code` and `request_id` when it is a
  `VaifError`.

Do not paste API keys, access tokens, passwords or customer data into an issue.

Report security vulnerabilities by email to security@vaif.studio, not in an
issue. See [SECURITY.md](SECURITY.md).

## Local development

Requirements: Python 3.10 through 3.14, and `git`.

```sh
git clone https://github.com/vaifstudio/vaif-python.git
cd vaif-python
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the same checks as CI:

```sh
python -m pytest                      # unit tests; HTTP is mocked with respx
python -m ruff check src tests        # lint
python -m ruff format --check src tests  # formatting; `ruff format src tests` fixes it
python -m mypy                        # strict type check
python -m build                       # wheel and sdist into dist/
python -m twine check --strict dist/*
```

CI also fails on any known vulnerability in the installed dependencies, and runs
the tests and the same scan with every dependency at its lowest allowed version
(the `lowest-dependencies` job in `.github/workflows/ci.yml`). To scan your
environment the same way:

```sh
python -m pip freeze --exclude-editable > installed.txt
python -m pip install pip-audit
python -m pip_audit --strict --no-deps --disable-pip --requirement installed.txt
```

The integration tests in `tests/test_integration.py` run against a real VAIF
Studio API and are skipped unless `VAIF_IT_BASE_URL`, `VAIF_IT_PROJECT_ID` and
`VAIF_IT_API_KEY` are set. Use a project created for testing: the tests create
users, rows and files.

### Generated code

`src/vaifstudio/_generated/` is generated from the VAIF Studio API's OpenAPI
description and is not edited by hand. Changes to it are made in the generator
upstream and arrive here with the next published change. The hand-written runtime
underneath it is `src/vaifstudio/_operations.py`.

## Pull requests

Pull requests are welcome. Keep each one focused on a single change, add or
update tests for it, and make sure the checks above pass.

The maintainers review every pull request. When a change is accepted, they apply
it in the upstream source tree with credit to you as a co-author, publish it here,
and close the pull request.

## Code of conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
