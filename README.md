# ACEest Fitness Gym 2025 (TM93112)

## Overview
ACEest Fitness Gym 2025 is a Flask-based web application developed as part of the DevOps CI/CD Implementation assignment for BITS Pilani WILP.  
The project demonstrates a **complete DevOps pipeline**, integrating **automation, testing, containerization, and orchestration** using industry-standard tools.

---

## Key Objectives
- Implement a CI/CD pipeline using **Git, Jenkins, Docker, SonarQube, and Kubernetes (Minikube)**.
- Automate build, test, and deployment workflows for continuous integration and delivery.
- Containerize the Flask application and deploy it in a local Kubernetes environment.
- Integrate Pytest and SonarQube for automated testing and code quality assurance.

---

## Tools and Technologies
| Category | Tool / Platform | Purpose |
|-----------|-----------------|----------|
| Version Control | Git & GitHub | Code tracking and collaboration |
| CI Server | Jenkins | Automation of build and test pipelines |
| Testing | Pytest | Unit and integration testing |
| Code Quality | SonarQube | Static analysis and quality gates |
| Containerization | Docker / Podman | Application packaging and deployment |
| Container Registry | Docker Hub | Storage and versioning of container images |
| Orchestration | Minikube / Kubernetes | Localized cloud-like deployment |

---

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/IMRaghvendraMishra/aceest-fitness-gym-2024tm93112.git
cd aceest-fitness-gym-2024tm93112
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Flask Application
```bash
python src/ACEest_Fitness.py
```

The app will start at:  
➡️ **http://127.0.0.1:5000**

---

## Testing

To run automated tests using **Pytest**:
```bash
pytest
```

---

## Docker Setup

### Build Docker Image
```bash
docker build -t aceest-fitness-gym .
```

### Run Docker Container
```bash
docker run -d -p 5000:5000 aceest-fitness-gym
```

### Access the Application
➡️ **http://localhost:5000**

---

## Jenkins CI/CD Pipeline

### Jenkinsfile Overview
The pipeline includes:
1. **Checkout Code** from GitHub  
2. **Install Dependencies**  
3. **Run Pytest** for automated testing  
4. **Static Code Analysis** using SonarQube  
5. **Build Docker Image**  
6. **Push Image** to Docker Hub  
7. **Deploy** to Kubernetes via Minikube  

---

## Kubernetes Deployment

### Start Minikube
```bash
minikube start
```

### Apply Deployment
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Verify Deployment
```bash
kubectl get pods
kubectl get svc
```

Access your app via:
```bash
minikube service aceest-fitness-gym-service
```

---

## CI/CD Pipeline Architecture

```text
Git → Jenkins (CI) → Pytest + SonarQube → Docker Build → Push to Docker Hub → Kubernetes (CD)
```

### Workflow Diagram
1. Developer commits code to GitHub.  
2. Jenkins triggers the pipeline automatically.  
3. Automated testing & code quality checks via Pytest and SonarQube.  
4. Docker image built and pushed to Docker Hub.  
5. Kubernetes pulls the latest image and deploys automatically.  

---

## Deployment Strategies Implemented
- **Blue-Green Deployment**
- **Rolling Updates**
- **Canary Release (optional)**
- **Rollback on Failure**

---

## Project Structure
```
aceest-fitness-gym-2024tm93112/
│
├── src/
│   ├── ACEest_Fitness.py
│   ├── ACEest_Fitness-V1.1.py
│   ├── ACEest_Fitness-V1.2.py
│   ├── ...
│
├── tests/
│   ├── test_app.py
│
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│
└── README.md
```

---

## References
1. [Flask Documentation](https://flask.palletsprojects.com/)
2. [Jenkins User Guide](https://www.jenkins.io/doc/)
3. [Docker Documentation](https://docs.docker.com/)
4. [Kubernetes Docs](https://kubernetes.io/docs/)
5. [SonarQube Docs](https://docs.sonarsource.com/)
6. [Pytest Documentation](https://docs.pytest.org/)
7. [GitHub Docs](https://docs.github.com/)
8. [Minikube Docs](https://minikube.sigs.k8s.io/)

---

## Author
**Raghvendra Mishra**  
WILP BITS Pilani | 2024TM93112  
Assignment: Introduction to DevOps (SEZG514)  
