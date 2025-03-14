# Raspberry Pi Setup: Git, Docker, and Flask Listener in Docker

This guide provides step-by-step instructions to **install Git**, **set up SSH for GitHub**, **configure Git**, **install Docker**, and **run a Flask listener inside a Docker container** on a Raspberry Pi.

---

## 🚀 **Step 1: Install Git on Raspberry Pi**
First, install **Git** to manage your code:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
```

### **Verify Installation**
```sh
git --version
```

---

## 🔑 **Step 2: Generate SSH Key for GitHub**
To securely push code to GitHub, generate an **SSH key**:

```sh
ssh-keygen -t ed25519 -C "your_personal_email@example.com"
```

When prompted:
- **Enter file in which to save the key:**  
- **Passphrase (optional):** Replace with your username of raspberry pi for `/home/your-username/.ssh/id_ed25519_github`
  ```sh
  /home/pi/.ssh/id_ed25519_github
  ```
- **Passphrase (optional):** Press **Enter** to skip or set a passphrase for security.

### **Copy and Add SSH Key to GitHub**
Copy the **public key** to your clipboard:

```sh
cat ~/.ssh/id_ed25519_github.pub
```

1. Go to **GitHub → Settings → SSH and GPG Keys**.
2. Click **New SSH Key**.
3. **Title:** `Raspberry Pi`
4. **Key type:** Authentication Key
5. **Paste the key** and click **Add SSH Key**.

### **Test the SSH Connection**
```sh
ssh -T git@github.com
```

If successful, you’ll see:

```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 🔧 **Step 3: Configure Git (Name & Email)**
Set up your **Git identity**:

```sh
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Verify your settings:

```sh
git config --list
```

---

## 📁 **Step 4: Create a Project Directory**
Now, create a folder for the project to store our pi server:

```sh
mkdir harvard_proj
cd harvard_proj
```

---

## 🐳 **Step 5: Install Docker on Raspberry Pi**
Docker allows you to containerize applications. Install it with:

```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### **Add User to Docker Group (Run Without `sudo`)**
```sh
sudo usermod -aG docker $USER
```

### **Reboot Raspberry Pi**
```sh
sudo reboot
```

### **Verify Docker Installation**
```sh
docker --version
```

---

## 🌐 **Step 6: Clone the Flask Listener Repository**
Now, **clone your GitHub repository** into the project folder:

```sh
git clone git@github.com:seintun/proj_pi_server.git
cd proj_pi_server
```


## Create virtual environment
```sh
python3 -m venv venv
```
Activate the virtual environment:
On macOS/Linux:
```sh
source venv/bin/activate
```
On Windows:
```sh
venv\Scripts\activate
```
Install packages:
```sh
pip install -r requirements.txt
```
---

## 🏰 **Step 7: Build and Run the Flask Listener in Docker**
### **Build the Docker Image**
```sh
docker build -t flask_listener .
```

### **Run the Flask Listener Container**
```sh
docker run -d -p 5001:5001 --name flask_listener flask_listener
```

---

## 🔍 **Step 8: Test the Flask Listener**
### **Check Running Containers**
```sh
docker ps
```

### **Test Locally on Raspberry Pi**
```sh
curl http://localhost:5001/action
```

Expected response:
```json
{"message": "Action executed on Raspberry Pi!"}
```

### **Test from Another Device (Laptop)**
Find Raspberry Pi's local IP:
```sh
hostname -I
```

From your **laptop**, run:
```sh
curl http://<Raspberry_Pi_IP>:5001/action
```

---

## ♻ **Step 9: Auto-Restart Flask Listener on Boot (Optional)**
To ensure the Flask listener runs after a reboot:

```sh
docker update --restart unless-stopped flask_listener
```

To restart manually:
```sh
docker restart flask_listener
```

---

## ❌ **Step 10: Remove All Docker (containers, images, networks, and volumes) (If Needed)**

To remove everything at once (containers, images, networks, and volumes), you can use:

```sh
docker system prune -a --volumes -f
```

---

## ♻️ **Maintenance Commands**

### **Stop Container**

```sh
docker stop flask_listener
```

### **Restart Container**

```sh
docker restart flask_listener
```

### **Remove Container**

```sh
docker rm flask_listener
```

### **Auto-Restart on Boot**

```sh
docker update --restart unless-stopped flask_listener
```

### **Remove Docker Resources**

Remove everything (containers, images, networks, and volumes):

```sh
docker system prune -a --volumes -f
```

---

## ✅ **Conclusion**
You have successfully:
✅ Installed **Git** and **Docker** on Raspberry Pi  
✅ Set up **SSH key authentication for GitHub**  
✅ Configured **Git with your name and email**  
✅ Cloned the project and **built the Flask listener in Docker**  
✅ Tested it locally and from another device  
✅ Set up **automatic restart on boot**  

---

🚀 **Your Raspberry Pi is now running a Flask API inside Docker!** 🎯  
For any issues, open a GitHub issue or contact me.  
Happy Coding! 🔦💪
