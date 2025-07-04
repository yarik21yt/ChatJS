# ChatJS

ChatJs - simple chat client that we (me and my friend) made using js and python with websockets.

## Installation

### Step 1. - Download source code
If you have git on your pc, you can tyype in cmd:

```bash
git clone https://github.com/yarik21yt/ChatJS.git
```
or just download from website :-)

### Step 2. - Installing something
you need to install:
- React JS
- Python (3.12 recommended)
- Redis (use chocolately for windows)

#### for python install that libraries:
sqlalchemy uvicorn fastapi redis websocket websockets
```python
pip install sqlalchemy uvicorn fastapi redis websocket websockets
```
(i recomend creating venv)




## Running
create 2 terminals for app and backend
```bash
cd app
```
--
```bash
cd backend
```
#### for frontend run:
```bash
npm run dev
```
#### in backend:
```bash
uvicorn main:app --reload
```

## DONE :D


# returns 'words'
foobar.pluralize('word')
