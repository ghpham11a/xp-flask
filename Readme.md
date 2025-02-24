# Commands

### Running locally

```sh
flask --app app run --debug
```

### Freeze requirements

```sh
pip freeze > requirements.txt
```

### Build Docker image

```sh
docker build -t xp-flask .
```

### Run the Docker container

```sh
docker run -p 80:80 xp-flask
```

### List running containers

```sh
docker ps
```

### Stop container

```sh
docker stop <container_id_or_name>
```

### Apply Kubernetes resources (inside k8s)

```sh
kubectl apply -f dev-deployment.yaml
kubectl apply -f dev-service.yaml
kubectl apply -f dev-secrets.yaml
```

### List running Kubernetes pods

```sh
kubectl get pods
```

### Inspect pod logs

```sh
kubectl describe pod <pod-name>
```

### Delete resoruces

```sh
kubectl delete service xp-flask-service
kubectl delete deployment xp-flask-deployment
kubectl delete secrets dev-secrets
kubectl delete pvc data-xp-postgres-postgresql-0
```

### Update Helm charts

```sh
helm repo update
```

### Install PostgreSQL Helm chart with custom values

```sh
helm install xp-postgres -f dev-postgres-values.yaml bitnami/postgresql
```

### Delete Helm chart

```sh
helm uninstall xp-postgres
```

### Connect to psql in Powershell

```sh
$POSTGRES_PASSWORD = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret --namespace default xp-postgres-postgresql -o jsonpath="{.data.postgres-password}")))

kubectl run xp-postgres-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:17.0.0-debian-12-r6 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host xp-postgres-postgresql -U postgres -d postgres -p 5432
```

### Connect to psql in bash

```sh
secret=$(kubectl get secret --namespace default xp-postgres-postgresql -o jsonpath="{.data.postgres-password}")

POSTGRES_PASSWORD=$(echo "$secret" | base64 --decode)

kubectl run -i --tty temp-psql-client --rm --restart='Never' \
  --image docker.io/bitnami/postgresql:17.0.0-debian-12-r6 \
  --env="PGPASSWORD=$POSTGRES_PASSWORD" \
  --command -- psql --host xp-postgres-postgresql -U postgres -d postgres -p 5432
```

### Encode secret in PowerShell for k8s secrets

```sh
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('secret-value'))
```

### Create table in psql

```sh
CREATE TABLE todos (id SERIAL PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL);
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT NOT NULL);
```

### list databases psql

```sh
\l
```

### Connect to database in psql

```sh
\c [DBNAME]
```

### Exit psql

```sh
\q
```

# Endpoints

localhost:80/todo