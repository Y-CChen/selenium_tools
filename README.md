# selenium_tools

###### tags: `selenium_tools`

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

### 2. selenium_tools

- install `.venv`
  - Development
    ```bash=
    poetry install --no-root
    ```
  - Production
    ```bash=
    poetry install --no-root --no-dev
    ```
