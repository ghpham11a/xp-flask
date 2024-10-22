# Commands

## Running locally

flask --app app run --debug

## Freeze requirements

pip freeze > requirements.txt

## Build Docker image

docker build -t xp-flask .

## Run the Docker container

docker run -p 80:80 xp-flask

## List running containers

docker ps

## Stop container

docker stop <container_id_or_name>

## Apply Kubernetes deployment (inside k8s)

kubectl apply -f deployment.yaml

## Apply Kubernetes service (inside k8s)

kubectl apply -f service.yaml

## List running Kubernetes pods

kubectl get pods

## Insepct pod logs

kubectl describe pod <pod-name>

## Delete pods

kubectl delete service xp-flask-service
kubectl delete deployment xp-flask-deployment
