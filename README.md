# book-rag
## Installation
If you do not have Node.js installed, go to https://nodejs.org/en/download/package-manager
Create a virtual environment in python for two terminals

```
python -m venv venv
source venv/bin/activate
```

In the first terminal run: 
```
    npm install
    npm start
```

In the other terminal run this after creating and activating a virtual environment (this will start the flask server needed for converting pdf to text):
```
    pip install -r requirements.txt
    npm run start-flask
```

Note: I did get some deprecated dependencies, but it should be fine

To start coding on an issue:
1. Create a new branch, go to each issue, which has a development section associated with it
2. Click create a branch
3. In you terminal, use the command ``` git fetch --all ```
4. Then checkout your branch, with the command ``` git checkout branch-nam ```
