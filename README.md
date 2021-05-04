# Cardamage Backend with FastAPI

## Installation

Install virtualenv first time

```bash
python3 -m pip install virtualenv 
```
Initial env

```bash
python3 -m venv env 
```

activate env
```bash
# Linux and OS X 
source env/bin/activate 

# Window
.\env\Scripts\activate
```
## Start Project
```bash
# --reload for hot reload
uvicorn app.main:app --reload
```

## Dependencies 
manage create requirement
```bash
pip3 freeze > requirements.txt  
```
install packages
```bash
pip3 install -r requirements.txt
```

