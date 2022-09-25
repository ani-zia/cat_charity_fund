# QRKot - Pet Charity App

Ready-made API for charity projects: create simple projects for fundraising and register incoming donations with automatic netting of funds.

`Python 3.9` 
`FastAPI 0.78` 
`SQLAlchemy 1.4`

## Start & Usage

### Installing

```
git clone https://github.com/ani-zia/cat_charity_fund.git
```

```
cd cat_charity_fund
```

```
python3 -m venv venv && source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

```
touch .env
```

`.env` file example:

```
APP_TITLE=Кошачий благотворительный фонд (0.1.0)
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=somekey
```

### Introducing

Command to start project on local server:

```
uvicorn app.main:app
```

Swagger interface will be available on your localhost adress for discovering API's opportunetes: localhost/docs


---

Author Anya Simanova