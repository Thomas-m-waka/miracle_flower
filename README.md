# Miracle Flowers

## Installation

```bash
git clone <https://github.com/Thomas-m-waka/miracle_flower.git>
cd miracle-flowers
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Environment & Database

Create a `.env` file with the required Django and PostgreSQL settings, then run:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Run

```bash
python manage.py runserver
```
