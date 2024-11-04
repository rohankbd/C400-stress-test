# Major-Project-C400
# System Stress Testing and Monitoring Framework

A comprehensive framework for automated system stress testing, monitoring, and alerting across distributed virtual machines. This project implements a complete CI/CD pipeline with containerization support and automated analysis using AI.

## Architecture Overview

The system consists of three virtual machines with the following roles:

- **VM_0**: Monitoring server (Prometheus, Grafana, Alertmanager)
- **VM_1**: Testing node (Node Exporter, MySQL Exporter, Stress Testing Script)
- **VM_2**: Database server (MySQL Server, Jenkins)

## Prerequisites

- CentOS 9 or compatible Linux distribution
- Ansible
- Docker and Kubernetes
- Python 3.x
- Jenkins
- Git
- Ngrok

## Initial Setup

### 1. Virtual Machine Configuration

```bash
# Stop firewall on all VMs
systemctl stop firewalld

# Set hostname on each VM
systemctl set-hostname <vm_name>
```

### 2. Required Software Installation

#### Install stress-ng
```bash
sudo dnf install -y stress-ng
```

#### Install Python Dependencies
```bash
pip install python-dotenv
pip install psutil
sudo dnf install -y iperf3 sysbench
```

### 3. MySQL Server Setup

```bash
# Install MySQL
sudo dnf install -y mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Configure MySQL for remote access
mysql -u root -p

# Create user and grant privileges
CREATE USER '<remoteUSR>'@'%' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON *.* TO '<remoteUSR>'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# Create test database
CREATE DATABASE <stressTestDB>;
GRANT ALL PRIVILEGES ON <stressTestDB>.* TO '<remoteUSR>'@'%';
FLUSH PRIVILEGES;
```

Edit MySQL configuration:
```bash
sudo nano /etc/my.cnf
# Add:
[mysqld]
bind-address = 0.0.0.0
```

## Monitoring Setup

### 1. Alertmanager Configuration

Create `alertmanager.yml` with email notification settings:
```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'your-email@gmail.com'
  smtp_auth_username: 'your-email@gmail.com'
  smtp_auth_password: 'your-password'
  smtp_require_tls: true
```

### 2. Prometheus Rules

Configure alert rules in `rules.yml` for:
- CPU Usage (>80%)
- Memory Usage (>80%)
- Disk Usage (>80%)
- Network Traffic
- System Load
- MySQL QPS

## CI/CD Pipeline Setup

### 1. Jenkins Installation

```bash
# Install Java
yum install java-17-openjdk -y

# Add Jenkins repository
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

# Install and start Jenkins
yum install jenkins -y
systemctl start jenkins
systemctl enable jenkins
```

### 2. Ngrok Setup

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvf ngrok-v3-stable-linux-amd64.tgz
mv ngrok /usr/local/bin/
ngrok config add-authtoken <your_auth_token>
ngrok http 8080
```

### 3. Jenkins Configuration

```bash
# Configure Jenkins user
sudo usermod -s /bin/bash jenkins
sudo visudo  # Add: jenkins ALL=(ALL) NOPASSWD:ALL

# Set up SSH keys
sudo mkdir -p /var/lib/jenkins/.ssh
sudo chown -R jenkins:jenkins /var/lib/jenkins/.ssh
sudo chmod 700 /var/lib/jenkins/.ssh
```

## Containerization

### Docker Setup

Build the container:
```bash
docker build -t stress-test-app .
```

### Kubernetes Deployment

Apply the deployment:
```bash
kubectl apply -f deployment.yaml
kubectl create secret generic env-secret --from-env-file=.env
```

## Monitoring Dashboards

- Node Exporter Dashboard ID: 1860
- MySQL Dashboard ID: 7362

## Log Analysis and Notifications

The system includes automated log analysis using Google's Gemini API and WhatsApp notifications through Twilio. Configure the following environment variables:
- `GEMINI_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`

## Acknowledgments

- Node Exporter
- Prometheus
- Grafana
- Google Gemini API
- Twilio API