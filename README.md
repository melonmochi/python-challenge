# Python Challenge -Paradigma Digital. <http://eventos.paradigmadigital.com/python-challenge/>

English | [Español](./README-es_ES.md)

[![Build Status](https://dev.azure.com/melonmochi3/python-challenge/_apis/build/status/melonmochi3.python-challenge?branchName=master)](https://dev.azure.com/melonmochi3/python-challenge/_build/latest?definitionId=1?branchName=master)

## ⌨️ Development

```bash
git clone git@github.com:melonmochi/python-challenge.git
cd python-challenge
```

## 🏈 Install

Setup a virtual env to install the package (recommended):

```bash
python3 -m venv env
source ./env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🏃 Run

### 🗄️ Setup databases

You **DO NOT** need to provide local databases, by default it's connected to AWS RDS's postgreSQL databases.

In case you want to use your own dbs, you can setup them in the `config.py` file of the root directory:

```python
class PeopleConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'YOUR_PEOPLE_DB URL'


class PlacesConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'YOUR_PLACES_DB URL'
```

We used [PostgreSQL](https://www.postgresql.org/) in our dev environment, theoretically it could be any relational db.

### ⚓ Places Server

```bash
export FLASK_APP=app:places_app
flask run --port=8081
```

Open your browser and visit <http://127.0.0.1:8081> to visit the places's swagger page.

### 🤼 People Server

```bash
export FLASK_APP=app:people_app
flask run --port=8082
```

Open your browser and visit <http://127.0.0.1:8082> to visit the people's swagger page.

### 👑 GOT Server

```bash
export FLASK_APP=app:got_app
flask run --port=8083
```

Open your browser and visit <http://127.0.0.1:8083> to visit the GOT's swagger page.

## 🗺️ RoadMap

- Use Docker to build app container. <https://www.docker.com/>
- Use Kubernetes (K8s) as containers manager. <https://kubernetes.io/>

## 🤝 Contributing [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

We welcome all contributions.

## 🌍 License

[MIT](https://github.com/melonmochi/python-challenge/blob/master/LICENSE)
