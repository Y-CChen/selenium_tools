# poetry_template

###### tags: `poetry_template`

## installation

### 1. [poetry](https://pypi.org/project/poetry/)

- with `pip`
  ```bash=
  pip install poetry
  ```
- without `pip`
  ```bash=
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  ```

### 2. poetry_template

- install `.venv`
  - Development
    ```bash=
    poetry install --no-root
    ```
  - Production
    ```bash=
    poetry install --no-root --no-dev
    ```
