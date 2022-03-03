# AiFame

AiFame is Flask application made for the Microsoft Azure Trial Hackathon on DEV 2022.

## Run locally
```
docker run --name postgres --rm -p 5432:5432 -e POSTGRES_USER=appseed -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=appseed-flask -d postgres
docker build -t flaskapp .
docker run -p 5005:5005 flaskapp
```