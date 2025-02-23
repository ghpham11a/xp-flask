# If UnauthorizedAccess (Temporary) -> powershell.exe -ExecutionPolicy Bypass -File ./dev-setup.ps1
# If UnauthorizedAccess (Permanent) -> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 1. Update Helm repositories
helm repo update

# 2. Install the PostgreSQL release using Helm with your custom values
helm install xp-postgres -f ../k8s/dev-postgres-values.yaml bitnami/postgresql

# 3. Apply Kubernetes manifests for deployment, service, and secrets
kubectl apply -f ../k8s/dev-deployment.yaml
kubectl apply -f ../k8s/dev-service.yaml
kubectl apply -f ../k8s/dev-secrets.yaml

# Optional: Wait a few seconds for the resources (especially the secret and database) to be created
Start-Sleep -Seconds 30

# 4. Retrieve the PostgreSQL password from the Kubernetes secret
$secret = kubectl get secret --namespace default xp-postgres-postgresql -o jsonpath="{.data.postgres-password}"
$POSTGRES_PASSWORD = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($secret))
Write-Output "Retrieved POSTGRES_PASSWORD: $POSTGRES_PASSWORD"

# 5. Define the SQL commands to create the tables
$sqlCmd = @"
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY, 
    title TEXT NOT NULL, 
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL
);
"@

# 6. Run a temporary PostgreSQL client pod to execute the SQL commands
kubectl run xp-postgres-postgresql-client `
  --rm --tty -i --restart='Never' --namespace default `
  --image docker.io/bitnami/postgresql:17.0.0-debian-12-r6 `
  --env="PGPASSWORD=$POSTGRES_PASSWORD" `
  --command -- psql --host xp-postgres-postgresql -U postgres -d postgres -p 5432 -c "$sqlCmd"