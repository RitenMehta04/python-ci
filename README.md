# python-ci

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
uvicorn src.main:app --reload --port 8080

##After Done
deactivate

#For Test run go to the Root Dir.
python -m pytest -v


############### Note #################
Press Cmd + Shift + P
Type and select Python: Select Interpreter.
