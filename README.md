# AiFame

AiFame is web application made for the Microsoft Azure Trial Hackathon on DEV 2022. Don't waste your food again!

AiFame allows you to:
- Take a picture of your shopping and computer vision algorithms will analyze it for you to detect food automatically
- Manage your food inventory like quantity and expiration date

Try it live [here](http://aifame.azurewebsites.net)!

## Our tech stack
<img src="https://cdn.worldvectorlogo.com/logos/python-4.svg" title="Python" alt="Python Logo" width="70"/>&emsp;
<img src="https://cdn.worldvectorlogo.com/logos/docker.svg" title="Docker" alt="Docker Logo" width="80"/>&emsp;
<img src="https://cdn.worldvectorlogo.com/logos/azure-2.svg" title="Docker" alt="Azure Logo" width="80"/>&emsp;
<img src="https://cdn.worldvectorlogo.com/logos/gunicorn.svg" title="Docker" alt="Gunicorn Logo" width="100"/>&emsp;
<img src="https://cdn.worldvectorlogo.com/logos/html-1.svg" title="Docker" alt="HTML Logo" width="70"/>&emsp;
<img src="https://cdn.worldvectorlogo.com/logos/css-3.svg" title="Docker" alt="CSS Logo" width="70"/>&emsp;
<img src="https://cdn.worldvectorlogo.com/logos/logo-javascript.svg" title="Docker" alt="JS Logo" width="70"/>&emsp;

- The backend is built with Python Flask and containerized with Docker.
- Docker images are pushed to Azure Container Registry and deployed with Azure App Service
- User data are stored in Azure SQL Database 
- Images are uploaded to Azure Storage Account and analyzed with Azure Computer Vision

## Authors
- [andregri](https://github.com/andregri)
- [CaptainMich](https://github.com/CaptainMich)
- [Dadigno](https://github.com/Dadigno)