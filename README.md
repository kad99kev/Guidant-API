# Guidant 

Main repository can be found here: https://github.com/ELITA04/Guidant


## How to run?

1. Download the dependencies
```
pip install -r requirements.txt
```

2. Run the FastAPI app
```
uvicorn main:app --reload
```

3. Run ngrok
```
ngrok http 8000
```

4. Change the URL in the config of app

### You can also run it with Docker

1. Execute Docker Build
```docker build -t <tag> PATH```

2. Execute Docker Run
```docker run --name <name> --publish <outside_port>:80 <tag>```
