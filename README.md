# APICBASE

## Full-Stack Developer challenge assignment - Backend

Written by *Lucas Cavalcante*, 2021

## Project setup

This project requires `python>=3.8`.

After cloning the repository, create a virtual environmnet

```bash
virtualenv -p /usr/bin/python3.8 venv
```

> In case your python environmnet is different, use the output from `$which python3.8`

Activate the virtual environment

```bash
source venv/bin/activate
```

Install the project dependencies

```bash
pip install -r requirements.txt
```

Apply the migrations

```bash
python manage.py migrate
```

Finally, run the server

```bash
python manage.py runserver
```

The project should be running at <http://localhost:8000/api/>.

> Optionally, change the environment variable `DEBUG` to `True` for debugging information in the `.env` file.

### Run the tests

```bash
python manage.py test
```

### Check for Lint fixes

```bash
black .
```

## Utilization instructions

- `api/ingredients/`
  - **GET**: list all ingredients
  - **POST**: create a new ingredient
  - **PUT**: edit an ingredient information
  - **DELETE**: delete an ingredient from the list
- `api/recipes/`
  - **GET**: list all recipes
  - **POST**: create a new recipe
  - **PUT**: edit a recipe information
  - **DELETE**: delete a recipe from the list
- `api/recipes-formulas/`
  - **GET**: list all recipes formulas
  - **POST**: create a new recipe formula
  - **PUT**: edit a recipe formula information
  - **DELETE**: delete a recipe recipe from the list
- `api/recipes/<int:recipe_id>/details/`
  - **GET**: display the details of a recipe formula with `<recipe_id>`
- `api/recipes/<int:recipe_id>/cost/`
  - **GET**: display the details of a recipe formula with `<recipe_id>`
