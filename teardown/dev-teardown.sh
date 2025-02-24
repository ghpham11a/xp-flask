#!/usr/bin/env bash

# permission denied -> chmod +x dev-teardown.sh

# Exit immediately on error
set -e

echo "Deleting xp-flask-service..."
kubectl delete service xp-flask-service || echo "xp-flask-service not found or already deleted."

echo "Deleting xp-flask-deployment..."
kubectl delete deployment xp-flask-deployment || echo "xp-flask-deployment not found or already deleted."

echo "Deleting dev-secrets..."
kubectl delete secrets dev-secrets || echo "dev-secrets not found or already deleted."

# Scale down the statefulset to prevent replica conflicts before uninstalling Helm release
echo "Scaling down xp-postgres-postgresql statefulset to 0..."
kubectl scale statefulset xp-postgres-postgresql --replicas=0 || echo "StatefulSet xp-postgres-postgresql not found or already scaled down."

echo "Deleting persistent volume claim data-xp-postgres-postgresql-0..."
kubectl delete pvc data-xp-postgres-postgresql-0 || echo "PVC data-xp-postgres-postgresql-0 not found or already deleted."

echo "Uninstalling Helm release xp-postgres..."
helm uninstall xp-postgres || echo "Helm release xp-postgres not found or already uninstalled."

echo "Teardown complete."
