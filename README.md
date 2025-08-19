- Create python venv

> /opt/homebrew/bin/python3.12 -m venv .venv

- Use Venv

> . .venv/bin/activate

- Install libs

> pip install -r requirements.txt

> npm install -g azure-functions-core-tools@4 --unsafe-perm true

- Dev run

> func start

- Initialize alembic

> alembic init alembic

- run pytest

> pytest -v

- run recovery report

> create folder tests/coverage

> pytest --cov=. --cov-report=html:tests/coverage --cov-config=.coveragerc

> open index.html
