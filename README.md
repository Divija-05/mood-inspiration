# Mood Inspiration 🌈

A personal project that generates inspirational mood-based quotes using the OpenAI API and a beautiful UI. Deployed using Docker and Kubernetes.

## 🚀 Features
- AI-generated inspirational messages
- Mood-based interface
- Responsive frontend
- Dockerized and Kubernetes-ready

## 🛠️ Tech Stack
- Python
- Flask
- OpenAI API
- HTML/CSS
- Docker + Kubernetes

## 📦 Setup


1. GitHub Setup


Step 1: Create a public/private GitHub repository 

Step 2: Cloning the Repository to the local system
git clone https://github.com/Divija-05/mood-inspiration.git
cd mood-inspiration

Step 3: Setting up the project in the GitHub folder
python3 -m venv venv
source venv/bin/activate 
pip3 install flask

Step 4: Create the flask app 

Step 5: Run and check the app if it is running
Python3 app.py

Step 6: Setting up gitnore and pushing the code to repo
echo "venv/" >> .gitignore
echo "\_\_pycache\_\_/" >> .gitignore



2. Setting up Docker and Kubernetes
Docker
Installing docker and running

Kubernetes
Step 1: Install homebrew if not installed and then install minikube
For installing brew : /bin/bash -c "$(curl -fsSL )"
For installing minikube : brew install minikube

Step 2 : Verification
Start minikube : minikube start --driver=docker
Check if minikube is working : minikube status
Set kubectl to use minikube : kubectl config use-context minikube
Verify Kubernetes is working: kubectl get nodes



3. Deployment

Step 1: Building docker image
touch Dockerfile
nano Dockerfile
docker build -t mood-inspiration-app .

Step 2: Check if the docker image is built
docker images

Step 4: Check on local host using docker
docker run -p 5001:5000 mood-inspiration-app

Step 5: Load the image into minikube
minikube image load mood-inspiration-app
eval $(minikube docker-env)
docker build -t mood-inspiration-app .
docker images | grep mood-inspiration-app

Step 6: Create service.yaml

Step 7: Create Kubernetes deployment (create deployment.yaml)
touch deployment.yaml
nano deployment.yaml

Step 6: Apply the deployment
kubectl apply -f deployment.yaml
kubectl get pods

Step 7: Expose the app and getting URL
kubectl apply -f service.yaml
kubectl get services
minikube service  --url (get the service name from the previous command)
minikube service mood-inspiration-service --url

Step 6: Create Kubernetes Secret 
echo -n "your\_openai\_api\_key\_here" | base64

kubectl apply -f secret.yaml



3. Auto Scaling
Step 1: Creating the metrics-server.yaml

Step 2: Checking metrics server status
kubectl get deployment metrics-server -n kube-system

Step 2: Applying autoscaling [using CLI (kubectl autoscale) instead of hpa.yaml]
kubectl autoscale deployment mood-inspiration-deployment --cpu-percent=50 --min=2 --max=5
kubectl get hpa



4. Rolling updates and rollback
Step 1: Check current deployment
kubectl get deployment mood-inspiration-deployment -o yaml | grep image
- image: mood-inspiration-app

Step 2: Build and push a new image
docker build -t your-dockerhub-username/mood-inspiration-app:v2 .
docker push your-dockerhub-username/mood-inspiration-app:v2

Step 3: Performing a rolling update
kubectl set image deployment/mood-inspiration-deployment mood-inspiration-app=your-dockerhub-username/mood-inspiration-app:v2
kubectl rollout status deployment mood-inspiration-deployment
kubectl get pods -w

Step 4: Verify the update
kubectl describe deployment mood-inspiration-deployment | grep Image
kubectl get pods

Step 5: Simulate a failure and rollback
kubectl rollout undo deployment mood-inspiration-deployment
kubectl rollout history deployment mood-inspiration-deployment



5. Logging
Step 1: Monitoring the pods
kubectl get pods

Step 2: Log a pod’s details
kubectl logs mood-inspiration-deployment-8648967fbb-4kx79

Step 2 : Live monitoring of a pod
kubectl logs -f mood-inspiration-deployment-8648967fbb-4kx79



6. Test Scenarios

1. Application Availability Tests
Test: Check if the application is accessible via the Kubernetes service. 
Command:
kubectl get services
minikube service mood-inspiration-service –url
Expected Output: Should return the homepage or API response of the application. 


2. Scaling Tests 
Test: Trigger high CPU usage to see if the Horizontal Pod Autoscaler (HPA) scales up pods.
Command: 
kubectl get hpa
kubectl run --rm -it --image=busybox stress-test -- /bin/sh
Inside BusyBox shell: 
while true; do wget -q -O- http://10.98.193.102:80; done 

Expected Output: Number of pods should increase dynamically. 
Verification: kubectl get pods -w


3. Rolling Update & Rollback Test
Test: Perform a rolling update and verify zero downtime. 
Command:
kubectl set image deployment/mood-inspiration-deployment mood-inspiration-app=your-dockerhub-username/mood-inspiration-app:v2
kubectl rollout status deployment/mood-inspiration-deployment
kubectl get pods -w
Expected Output: New version is deployed while keeping the app running. 

Test: Rollback to the previous version in case of failure. 
Command: 
kubectl rollout undo deployment/mood-inspiration-deployment
kubectl rollout history deployment/mood-inspiration-deployment
Expected Output: Application reverts to the previous working version. 


4. Pod Failure and Self-Healing Test 
Test: Manually delete a pod and check if Kubernetes automatically recreates it. 
 Command: 
kubectl delete pod 
kubectl delete pod mood-inspiration-deployment-8648967fbb-4kx79 
Verification: kubectl get pods -w
Expected Output: A new pod should be automatically created. 


5. Logging Test 
Test: Check if application logs are available. 
Command: 
kubectl get pods
kubectl logs mood-inspiration-deployment-8648967fbb-6r897
Expected Output: Should display application logs. 








