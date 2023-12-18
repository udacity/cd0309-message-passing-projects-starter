# k3s: Lightweight Kubernetes
```shell
# Install
curl -sfL https://get.k3s.io | sh -

# Config kubectl
sudo cp /etc/rancher/k3s/k3s.yaml /home/${USER}/.kube/config
sudo chown ${USER} ~/.kube/config
chmod 600 ~/.kube/config

```

# Argocd: Declarative continuous delivery with a fully-loaded UI

https://argo-cd.readthedocs.io/en/stable/getting_started
## Install Argo CD¶
```shell
# namespace argocd
kubectl create namespace argocd

# apply
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

```
## Access The Argo CD API Server

```shell
# Service Type Load Balancer
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

# Port Forwarding
kubectl port-forward svc/argocd-server -n argocd 8080:443

```

## Download Argo CD CLI
```shell
Download the latest Argo CD version from https://github.com/argoproj/argo-cd/releases/latest. More detailed installation instructions can be found via the CLI installation documentation.
```

## Login Using The CLI
```shell
# The initial password for the admin account is auto-generated and stored as clear text in the field password in a secret named argocd-initial-admin-secret in your Argo CD installation namespace. You can simply retrieve this password using the argocd CLI:
argocd admin initial-password -n argocd

# Using the username admin and the password from above, login to Argo CD's IP or hostname:
argocd login <ARGOCD_SERVER>

# Change the password using the command:
argocd account update-password

```

# Helm: The package manager for Kubernetes
https://helm.sh

## Install Helm

https://helm.sh/docs/intro/install/

```shell

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

```

## Helm cheatsheet

https://helm.sh/docs/intro/cheatsheet/

# Prometheus: Monitoring system & time series database

https://prometheus.io/


# Grafana: open source, distributed tracing platform

https://grafana.com/


# Jaeger: open source, distributed tracing platform

https://www.jaegertracing.io/

# gRPC: A high performance, open source universal RPC framework

https://grpc.io/

## gRPC Python

https://grpc.io/docs/languages/python/quickstart/

```

```

# Postgres

```shell

kubectl apply -f deployment/db-configmap.yaml

kubectl apply -f deployment/db-secret.yaml

kubectl apply -f deployment/postgres.yaml

```