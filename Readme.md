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

## Apply Kubernetes resources (inside k8s)

kubectl apply -f dev-deployment.yaml
kubectl apply -f dev-service.yaml
kubectl apply -f dev-secrets.yaml

## List running Kubernetes pods

kubectl get pods

## Inspect pod logs

kubectl describe pod <pod-name>

## Delete resoruces

kubectl delete service xp-flask-service
kubectl delete deployment xp-flask-deployment
kubectl delete secrets dev-secrets
kubectl delete pvc data-xp-postgres-postgresql-0

## Update Helm charts

helm repo update

## Install PostgreSQL Helm chart with custom values

helm install xp-postgres -f dev-postgres-values.yaml bitnami/postgresql

## Delete Helm chart

helm uninstall xp-postgres

## Connect to db

$POSTGRES_PASSWORD = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret --namespace default xp-postgres-postgresql -o jsonpath="{.data.postgres-password}")))

kubectl run xp-postgres-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:17.0.0-debian-12-r6 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host xp-postgres-postgresql -U postgres -d postgres -p 5432

## Encode secret in PowerShell

[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('secret-value'))

## Create table

CREATE TABLE todos (id SERIAL PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL);
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT NOT NULL);