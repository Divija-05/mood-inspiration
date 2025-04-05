
## 🚀 Features
- AI-generated inspirational messages
- Mood-based interface
- Responsive frontend
- Dockerized and Kubernetes-ready

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask, OpenAI API  
- **Frontend:** HTML/CSS  
- **Deployment:** Docker, Kubernetes  

---

## GitHub Setup

### Step 1: Create a GitHub Repository
Create a public/private repository on GitHub.

### Step 2: Clone the Repository Locally
```
git clone https://github.com/Divija-05/mood-inspiration.git
cd mood-inspiration
```

### Step 3: Set Up the Project Environment
```
python3 -m venv venv
source venv/bin/activate 
pip3 install flask
```

### Step 4: Create the Flask App  
Develop your Flask application.

### Step 5: Run the Application Locally
```
python3 app.py
```

### Step 6: Configure `.gitignore` and Push Code to GitHub  
```
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
```

---

## Setting Up Docker and Kubernetes

### Docker Setup  
Install Docker and ensure it is running.

### Kubernetes Setup  
#### Step 1: Install Minikube  
Install Homebrew (if not already installed):  
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Install Minikube:  
```
brew install minikube
```

#### Step 2: Verify Minikube Installation  
Start Minikube:
```
minikube start --driver=docker
```
Check Minikube status:
```
minikube status
```
Set `kubectl` to use Minikube:
```
kubectl config use-context minikube
```
Verify Kubernetes functionality:
```
kubectl get nodes
```

---

## Deployment

### Step 1: Build Docker Image  
Create a `Dockerfile`:
```
touch Dockerfile && nano Dockerfile
docker build -t mood-inspiration-app .
```

### Step 2: Verify Docker Image Build  
```
docker images
```

### Step 3: Run Locally Using Docker  
```
docker run -p 5001:5000 mood-inspiration-app
```

### Step 4: Load Image into Minikube  
```
minikube image load mood-inspiration-app 
eval $(minikube docker-env)
docker build -t mood-inspiration-app .
docker images | grep mood-inspiration-app
```

### Step 5: Create Kubernetes Deployment Files  
Create `deployment.yaml` and `service.yaml`:
```
touch deployment.yaml && nano deployment.yaml 
touch service.yaml && nano service.yaml 
```

### Step 6: Apply Deployment  
```
kubectl apply -f deployment.yaml 
kubectl get pods 
kubectl apply -f service.yaml 
kubectl get services 
minikube service mood-inspiration-service --url 
```

### Step 7: Set Up Kubernetes Secret  
Encode API key:
```
echo -n "your_openai_api_key_here" | base64 
kubectl apply -f secret.yaml 
```

---

## Auto Scaling

### Step 1: Deploy Metrics Server  
Create `metrics-server.yaml` and deploy it.

### Step 2: Verify Metrics Server Status  
```
kubectl get deployment metrics-server -n kube-system 
```

### Step 3: Apply Autoscaling via CLI  
```
kubectl autoscale deployment mood-inspiration-deployment --cpu-percent=50 --min=2 --max=5 
kubectl get hpa 
```

---

## Rolling Updates & Rollbacks

### Rolling Update  
#### Step 1: Build and Push New Image  
```
docker build -t your-dockerhub-username/mood-inspiration-app:v2 .
docker push your-dockerhub-username/mood-inspiration-app:v2 
```

#### Step 2: Perform Rolling Update  
```
kubectl set image deployment/mood-inspiration-deployment mood-inspiration-app=your-dockerhub-username/mood-inspiration-app:v2 
kubectl rollout status deployment mood-inspiration-deployment 
kubectl get pods -w 
```

#### Verify Update Status:
```
kubectl describe deployment mood-inspiration-deployment | grep Image 
kubectl get pods 
```

### Rollback in Case of Failure  
```
kubectl rollout undo deployment mood-inspiration-deployment 
kubectl rollout history deployment mood-inspiration-deployment 
```

---

## Logging

### Monitor Pods Status  
```
kubectl get pods 
```

### View Logs for a Pod  
```
kubectl logs mood-inspiration-deployment-8648967fbb-4kx79 
```

### Live Monitoring of Pod Logs  
```
kubectl logs -f mood-inspiration-deployment-8648967fbb-4kx79 
```

---

## Test Scenarios  

### 1. Application Availability Test  
**Command:**  
```
kubectl get services 
minikube service mood-inspiration-service --url 
```  

**Expected Output:** Homepage or API response of the application.

---

### 2. Scaling Test  
**Command:** Trigger high CPU usage inside BusyBox shell:
```
while true; do wget -q -O- http://10.98.193.102:80; done 
```  

**Verification:** Pods should scale dynamically.
```
kubectl get hpa 
kubectl get pods -w 
```  

---

### 3. Rolling Update & Rollback Test  

#### Rolling Update Command:
```
kubectl set image deployment/mood-inspiration-deployment mood-inspiration-app=your-dockerhub-username/mood-inspiration-app:v2 
kubectl rollout status deployment mood-inspiration-deployment 
kubectl get pods -w 
```  

**Expected Output:** Zero downtime during update.

#### Rollback Command:
```
kubectl rollout undo deployment/mood-inspiration-deployment 
kubectl rollout history deployment/mood-inspiration-deployment 
```  

**Expected Output:** Application reverts to the previous version.

---

### 4. Pod Failure & Self-Healing Test  

**Command:** Delete a pod manually:
```
kubectl delete pod mood-inspiration-deployment-8648967fbb-4kx79 
```  

**Verification:** A new pod should be automatically created.
```
kubectl get pods -w 
```  

---

### 5. Logging Test  

**Command:** View logs for a pod:
```
kubectl logs mood-inspiration-deployment-8648967fbb-6r897 
```  

**Expected Output:** Application logs are displayed.
"""

