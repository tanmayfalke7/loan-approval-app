# 🏦 Loan Approval Eligibility System

A containerized **Streamlit** web application that evaluates instant loan eligibility based on an applicant's financial profile, packaged with **Docker** and deployed on **Kubernetes** using Deployment and NodePort Service manifests.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Project File Structure](#-project-file-structure)
- [Prerequisites](#-prerequisites)
- [1. Local Setup (Without Docker)](#-1-local-setup-without-docker)
- [2. Docker Containerization](#-2-docker-containerization)
- [3. Kubernetes Deployment](#-3-kubernetes-deployment)
- [How It Works (Containerization & Deployment Flow)](#-how-it-works-containerization--deployment-flow)
- [Execution Evidence & Screenshots](#-execution-evidence--screenshots)

---

## 🔍 Overview

The application provides an interactive form where users enter:
- **Applicant Full Name**
- **Monthly Income ($)**
- **Credit Score (300–850)**
- **Employment Status** (`Salaried`, `Self-Employed`, `Unemployed`, `Student`)
- **Requested Loan Amount ($)**
- **Loan Tenure (Years)**
- **Existing Monthly Debt / EMI ($)**

Upon submission, the app calculates the estimated monthly EMI (at a 10% annual interest rate) and the projected **Debt-to-Income (DTI) ratio**, then determines loan eligibility against standard lending criteria (minimum credit score of 650, minimum income of $2,000, active employment, and DTI ratio $\le 45\%$).

---

## 📁 Project File Structure

```text
loan-approval-app/
├── app.py                  # Streamlit loan eligibility form and business logic
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-step instructions to build the Docker image
├── .dockerignore           # Files excluded from the Docker build context
├── README.md               # Project documentation and deployment guide
└── k8s/
    ├── deployment.yaml     # Kubernetes Deployment manifest (2 replicas + health probes)
    └── service.yaml        # Kubernetes NodePort Service manifest (exposes port 30080)
```

---

## 🛠 Prerequisites

Ensure the following tools are installed on your system:
- **Python 3.11+** (for local testing)
- **Docker Desktop** or **Docker Engine**
- **Kubernetes Cluster** (Docker Desktop Kubernetes, Minikube, or Kind)
- **kubectl** CLI configured to communicate with your cluster
- **Docker Hub Account** (to host the custom container image)

---

## 💻 1. Local Setup (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-github-username>/loan-approval-app.git
   cd loan-approval-app
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies and launch Streamlit:**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`.

---

## 🐳 2. Docker Containerization

1. **Build the custom Docker image:**
   *(Replace `<your-dockerhub-username>` with your actual Docker Hub username.)*
   ```bash
   docker build -t <your-dockerhub-username>/loan-approval-app:v1 .
   ```

2. **Verify the created image:**
   ```bash
   docker images
   ```

3. **Run the application inside a Docker container:**
   ```bash
   docker run -d -p 8501:8501 --name loan-app-container <your-dockerhub-username>/loan-approval-app:v1
   ```

4. **Verify the running container and test in browser:**
   ```bash
   docker ps
   ```
   Navigate to `http://localhost:8501` to confirm the form works inside the container.

5. **Stop and remove the standalone test container:**
   ```bash
   docker stop loan-app-container
   docker rm loan-app-container
   ```

6. **Push the image to Docker Hub:**
   ```bash
   docker login
   docker push <your-dockerhub-username>/loan-approval-app:v1
   ```

---

## ☸️ 3. Kubernetes Deployment

1. **Update the image name in `k8s/deployment.yaml`:**
   Open `k8s/deployment.yaml` and replace `your-dockerhub-username/loan-approval-app:v1` with your Docker Hub image tag.
   > *Note: If using Minikube locally without pushing to Docker Hub, run:*
   > ```bash
   > minikube image load <your-dockerhub-username>/loan-approval-app:v1
   > ```

2. **Apply the Deployment and Service manifests:**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

3. **Verify Deployments, Pods, and Services:**
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get svc loan-approval-service
   ```

4. **Access the deployed application:**
   - **Docker Desktop Kubernetes:** Open `http://localhost:30080` in your browser.
   - **Minikube:** Run the command below to automatically open the exposed service URL:
     ```bash
     minikube service loan-approval-service
     ```

5. **Clean up Kubernetes resources (when finished):**
   ```bash
   kubectl delete -f k8s/service.yaml
   kubectl delete -f k8s/deployment.yaml
   ```

---

## ⚙️ How It Works (Containerization & Deployment Flow)

1. **Containerization (`Dockerfile`):** Uses the lightweight `python:3.11-slim` base image, installs Streamlit from `requirements.txt`, copies `app.py`, configures a `HEALTHCHECK` against Streamlit's `/_stcore/health` endpoint, and binds the server to `0.0.0.0:8501`.
2. **Orchestration (`k8s/deployment.yaml`):** Launches **2 Pod replicas** of the container for high availability, enforces CPU/memory resource limits, and uses HTTP liveness and readiness probes to automatically restart unhealthy containers.
3. **Service Exposure (`k8s/service.yaml`):** Creates a `NodePort` Service that maps external cluster traffic on port `30080` to port `8501` across the running application Pods.

---

## 📸 Execution Evidence & Screenshots

> *Add your assignment screenshots in a `screenshots/` folder and link them below before final submission:*

- **Docker Image Build & Running Container (`docker ps`):**  
  `![Docker Run](screenshots/docker-run.png)`
- **Kubernetes Pods & Service Status (`kubectl get pods,svc`):**  
  `![Kubernetes Status](screenshots/k8s-status.png)`
- **Working Loan Approval Application UI:**  
  `![App Output](screenshots/app-ui.png)`