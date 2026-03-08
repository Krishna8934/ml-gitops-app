# ML GitOps App

This repository contains the **FastAPI machine learning application** used in the ML GitOps Automation Platform.

The application exposes API endpoints for prediction, health checks, and Prometheus metrics and is containerized using Docker for deployment in Kubernetes.

---

## Features

- FastAPI based ML API
- `/predict` endpoint for model inference
- `/health` endpoint for service health checks
- `/metrics` endpoint for Prometheus monitoring
- Dockerized application
- CI pipeline using GitHub Actions

---

## CI Pipeline

The repository includes a GitHub Actions workflow that:

1. Builds the Docker image
2. Pushes the image to Docker Hub
3. Updates the Kubernetes manifest repository with the new image tag

This triggers automatic deployment through GitOps.

---

## Docker Image

Example Docker image: krishna23243/ml-gitops-app:latest

---

## Related Repositories

Main project documentation:

https://github.com/Krishna8934/ml-gitops-platform

Kubernetes manifests repository:

https://github.com/Krishna8934/ml-gitops-manifests

---

## Live Application

https://ml-gitops-app.onrender.com