# If UnauthorizedAccess (Temporary) -> powershell.exe -ExecutionPolicy Bypass -File ./dev-teardown.ps1
# If UnauthorizedAccess (Permanent) -> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

kubectl delete service xp-flask-service
kubectl delete deployment xp-flask-deployment
kubectl delete secrets dev-secrets
kubectl delete pvc data-xp-postgres-postgresql-0

# Need to scale down or resource will replicate and prevent helm uninstall
kubectl scale statefulset xp-postgres-postgresql --replicas=0

helm uninstall xp-postgres