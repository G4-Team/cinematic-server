# cinematic-server

## Getting Started
1. Clone this repository to your local machine:
```
git clone https://github.com/G4-Team/cinematic
```
2- SetUp a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
3- install Dependencies
```
pip install -r requirements.txt
```
4- create your .env file and complete variables.
```
cp .env.example .env
```
5- Create tables in database
```
python manager.py migrate
```
6- start server and run the project
```
python manager.py runserver
```
