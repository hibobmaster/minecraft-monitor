
## development
Create virtual environment and install dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Debug the code
```
uvicorn main:app --reload
```

## deployment
```
uvicorn main:app --host "127.0.0.1" --port 10010 --proxy-headers --forwarded-allow-ips "*"
```
