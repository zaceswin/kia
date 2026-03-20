# kia
failed server access 
# 🔐 Failed Pentest Simulation

## 📌 Overview

This repository demonstrates a **safe simulation of a failed penetration test** from a server's perspective.

Instead of performing real attacks, the scripts show how a system:

* Handles unauthorized login attempts
* Logs suspicious activity
* Denies access to invalid credentials

This project is designed for **educational purposes only**, focusing on **defensive security practices (blue team perspective)**.

---

## 🎯 Objectives

* Simulate multiple failed login attempts
* Demonstrate basic logging mechanisms
* Show how servers respond to unauthorized access
* Provide beginner-friendly cybersecurity examples

---

## 🛠️ Technologies Used

* **Python** – for readable and structured simulation
* **C** – for low-level system-style implementation
* **Bash** – for scripting and automation

---

## 📂 Project Structure

```
failed-pentest-simulation/
│── failed_pentest_simulation.py
│── failed_pentest_simulation.c
│── failed_pentest_simulation.sh
│── server_logs.txt
│── README.md
```

---

## ▶️ How to Run

### 🐍 Python

```bash
python3 failed_pentest_simulation.py
```

### ⚙️ C

```bash
gcc failed_pentest_simulation.c -o pentest_sim
./pentest_sim
```

### 🖥️ Bash

```bash
chmod +x failed_pentest_simulation.sh
./failed_pentest_simulation.sh
```

---

## 📊 What the Simulation Shows

* Repeated login attempts using weak/common credentials
* Server rejecting invalid authentication
* Logging of failed access attempts with timestamps
* No successful breach (pentest fails)

---

## ⚠️ Disclaimer

This project **does NOT perform real hacking or exploitation**.
It is strictly for:

* Learning purposes
* Demonstrating security concepts
* Showcasing defensive programming

Do not use these concepts for unauthorized access to systems.

---

## 🚀 Future Improvements

* Add account lockout after multiple failed attempts
* Simulate IP tracking and blocking
* Create a log analyzer dashboard
* Expand to web-based authentication simulation

---

## 👨‍💻 Author
zaceswin/   
Created as part of a cybersecurity learning journey/project


---

## ⭐ Contribute

Feel free to fork this repository, improve the simulation, and submit a pull request!
