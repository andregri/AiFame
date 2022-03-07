# AiFame

AiFame is Flask application made for the Microsoft Azure Trial Hackathon on DEV 2022.

## Run locally
```
docker run --name postgres --rm -p 5432:5432 -e POSTGRES_USER=appseed -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=appseed-flask -d postgres
gunicorn -w 1 run:app
```

## Run with docker
```
docker run --name postgres --rm -p 5432:5432 -e POSTGRES_USER=appseed -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=appseed-flask -d postgres
docker build -t flaskapp --target dev .
docker run -e DEPLOY_ENVIRONMENT="Development" -p 5005:5005 flaskapp
```

## Build production Docker image
```
docker build -t prodapp --file Dockerfile.prod .
docker run -e DEPLOY_ENVIRONMENT="Production" -p 5005:5005 prodapp
```

## Upload production image
```
docker build -t aifame --file Dockerfile.prod .
docker login aifame.azurecr.io 
docker tag aifame aifame.azurecr.io/aifame
docker push aifame.azurecr.io/aifame
```