### **README.md**

```markdown
# ACEest Fitness - DevOps CI/CD Project

## 🚀 Overview
**ACEest Fitness** is a Flask-based web application containerized using Docker and deployed to a Kubernetes cluster.  
This project demonstrates a complete **CI/CD pipeline** using **Jenkins**, **SonarQube**, **Pytest**, and **DockerHub** integration — ensuring automated testing, static code analysis, and continuous delivery.

---

## CI/CD Architecture

### Tools Used:
| Tool | Purpose |
|------|----------|
| **Jenkins** | CI/CD pipeline automation |
| **SonarQube** | Static code analysis and quality gate enforcement |
| **Docker** | Containerization and image versioning |
| **Kubernetes (Minikube)** | Deployment and orchestration |
| **Pytest** | Unit testing |
| **GitHub** | Source code management |

### Pipeline Stages:
1. **Checkout** – Pull latest code from GitHub  
2. **Unit Test** – Run Pytest and generate test reports  
3. **SonarQube Analysis** – Perform static code analysis  
4. **Quality Gate** – Wait for SonarQube quality gate approval  
5. **Docker Build & Push** – Build and push Docker image to DockerHub  
6. **Deploy to Kubernetes** – Apply deployment and service manifests

---

## Project Structure
```

ACEest-DevOps/
│
├── ACEest_Fitness.py           # Flask application
├── requirements.txt            # Dependencies
├── tests/
│   └── test_app.py             # Pytest test cases
│
├── Dockerfile                  # Docker image build file
├── Jenkinsfile                 # Jenkins pipeline configuration
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
│
├── reports/
│   ├── junit.xml
│   └── coverage.xml
│
└── README.md                   # Project documentation

````

---

## Testing and Quality

### Run Tests Locally:
```bash
pytest -q --junitxml=reports/junit.xml --cov=app --cov-report=xml:reports/coverage.xml
````

### SonarQube Analysis:

The pipeline uses:

```
sonar-scanner \
  -Dsonar.projectKey=ACEest-Fitness \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<SONAR_TOKEN>
```

---

## Docker

### Build & Run:

```bash
docker build -t sujitagupta/aceest-fitness:latest .
docker run -d -p 5000:5000 sujitagupta/aceest-fitness:latest
```

### Push to DockerHub:

```bash
docker push sujitagupta/aceest-fitness:latest
```

---

## Kubernetes Deployment

### Apply Resources:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

### Get Service Endpoint:

```bash
kubectl get svc -n aceest
```

If using **Minikube**, run:

```bash
minikube ip
```

Then access:

```
http://<MINIKUBE_IP>:<NODE_PORT>
```

Example:

```
http://192.168.49.2:31245
```

---

## Important URLs

| Component                                  | URL                                                                                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **GitHub Repository**                      | [https://github.com/Sujitagupta/ACEest-Fitness-DevOps-assignment2](https://github.com/Sujitagupta/ACEest-Fitness-DevOps-assignment2)       |
| **DockerHub Repository**                   | [https://hub.docker.com/repository/docker/sujitagupta/aceest-fitness](https://hub.docker.com/repository/docker/sujitagupta/aceest-fitness) |
| **SonarQube Dashboard**                    | `http://localhost:9000/dashboard?id=ACEest-Fitness`                                                                                        |
| **Kubernetes Endpoint (NodePort/Ingress)** | *Will show after deployment*                                                                                                               |

---

## Challenges & Solutions

| Challenge                        | Mitigation Strategy                                                                     |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| SonarQube webhook unreachable    | Reconfigured webhook to use correct host IP instead of loopback                         |
| Docker credential helper missing | Installed `docker-credential-desktop` and used full Docker path `/usr/local/bin/docker` |
| Jenkins SonarQube timeout        | Increased quality gate timeout and verified webhook                                     |
| K8s service not exposed          | Switched to NodePort service for external access                                        |

---

## Key Automation Outcomes

* Fully automated build-test-deploy workflow
* Static code analysis integrated into CI pipeline
* Test coverage reporting using Pytest + SonarQube
* Docker image versioning on DockerHub
* Kubernetes-based continuous delivery

---

## Author

**Sujita Gupta**
DevOps Assignment – ACEest Fitness

