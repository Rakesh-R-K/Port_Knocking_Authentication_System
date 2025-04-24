# 🔐 Port Knocking Authentication System

A lightweight and secure authentication mechanism to hide and control access to the SSH service. This project uses `knockd` and `iptables` to implement port knocking on a Kali Linux server, allowing only authorized clients to access SSH after sending a specific sequence of TCP knocks.

---

## 🧠 Overview

- **Server:** Kali Linux (running `knockd` and SSH)
- **Client:** Any OS (Tested on Windows using `knock` client)
- **Security Approach:** Ports are closed by default. SSH port opens **only** when a valid port knock sequence is detected, and relocks after a timeout or reverse knock.

---

## ⚙️ Features

- 🔐 Hide SSH port behind port knocking
- 🧱 Dynamic firewall rule manipulation using `iptables`
- 🔁 Auto relocking after knock or timeout
- 🕵️ IP logging of all knock attempts
- 🖥️ Cross-platform client support

---

## 🛠️ Setup

### 📌 Requirements

- `knockd`
- `iptables`
- `netfilter-persistent`
- `openssh-server`

### 🚀 Installation (on Kali Linux Server)

```bash
sudo apt update
sudo apt install knockd netfilter-persistent openssh-server
```

### 🔒 Block SSH Port by Default

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j DROP
sudo netfilter-persistent save
```

### 📝 Configure knockd

Edit the config file:

```bash
sudo nano /etc/knockd.conf
```

Add the following:

```ini
[options]
    logfile = /var/log/knockd.log

[openSSH]
    sequence = 4000,3000,2000
    seq_timeout = 15
    command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags = syn

[closeSSH]
    sequence = 2000,3000,4000
    seq_timeout = 15
    command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags = syn
```

Enable and start the service:

```bash
sudo systemctl enable knockd
sudo systemctl start knockd
```

### 💻 Client Usage

#### 🔁 Send Knock Sequence (from Windows/Linux/macOS)

```bash
knock <server-ip> 4000 3000 2000
```

#### 🔓 Connect via SSH (after knock)

```bash
ssh username@<server-ip>
```

---

## 📂 File Structure

```
📁 port-knocking-auth
├── README.md
├── knockd.conf (optional: your custom config)
├── screenshots/ (optional: usage demo)
└── docs/ (optional: detailed documentation)
```

---

## 🔒 Security Add-ons (Suggestions)

- Add a cron job to re-lock port after X seconds
- Use reverse knock sequence to manually close access
- Log invalid knock attempts and alert admin
- Combine with SSH key-based authentication for extra security
- Added a python script for server to track the requests

---

## 📜 License

This project is open-source and free to use for academic and educational purposes.
