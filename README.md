# TP2_Devops
## Author : Emile EKANE
## Date : 2020-06-12

## Docs

> Retrouvez l'exercice précédent sur ce [lien] (https://github.com/ekane3/TP1_Devops) pour plus de contexte.

- Configuration d'un workflow GitHub Action qui build et push automatiquement l'image sur DockerHub a chaque nouveau commit.  

```yaml
# This is a basic workflow to help you get started with Actions

name: Weather_app CI-CD  workflow TP2 

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "main" branch
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # A job named push_to_registry to push our Docker image to Docker Hub
  push_to_registry:
    name: Push Docker Image to Docker Hub
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - name: Check out the repo
        uses: actions/checkout@v3

      # Login to Docker Hub
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with: 
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}
      
      # Build and push docker image
      - name: Build docker image
        # Runs a set of commands using the runners shell
        run: | 
          echo "****Eat some 🍔🍔"
          if [ $(docker run --rm -i hadolint/hadolint < dockerfile | wc -l) -eq 0 ]
          then 
            docker build -t $USERNAME/efrei-devops-tp2:$VERSION .
            docker push $USERNAME/efrei-devops-tp2:$VERSION
            echo ✔ YOUR CODE HAVE BEEN PUSHED SUCCESSFULLY
          else
            echo ❌FAIL !!! CHECK YOUR Dockerfile
          fi
        env:
          USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
          VERSION: latest

  # This workflow contains a single job called "build" .
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v3

      # Runs a single command using the runners shell
      - name: Run a one-line script
        run: echo Hello, world!

      # Runs a set of commands using the runners shell
      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.

```  

- Transformons notre wrapper en API
```python
import requests
import json
import os

from flask import Flask, render_template, request

app = Flask(__name__)

# create a function that returns the weather for a specific location using env lat and lon
@app.route('/')
def index( ):
    args = request.args
    
    lat = args['lat']
    lon = args['lon']
    api_key = os.environ['API_KEY']
    
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}').text
    
    return f"{res}\n"

if __name__ == "__main__":
    app.run(host="localhost", port=8081, debug=True)
```


### Pour éxecuter l'api.

- Run API qui renvoie la météo en utilisant la commande suivant en utilisant notre image:  

1ère commande:
```cmd
docker run --network host --env API_KEY=**** ekane3/efrei-devops-tp2:latest
```   

2ème commande:
```cmd
curl "http://localhost:8081/?lat=5.902785&lon=102.754175"
```


### Error

On n'a pas arrivé a faire tourner l'image sur le port 8081 avec cURL sur OS : Windows 10. 


### Important links
- DockerHub : https://hub.docker.com/repository/docker/ekane3/efrei-devops-tp2  

- Lien GitHub : https://github.com/ekane3/TP2_Devops