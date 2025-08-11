# Agro-AI

**CSCI 4970 Capstone Project**

This project aims to build trust among farmers in artificial intelligence by demonstrating an interactive learning system. Users will provide input to a machine learning algorithm and observe how their feedback impacts its accuracy.

---

## Project Overview

- **Core Functionality:**  
  Users will interact with a web-based interface to label images of corn as either healthy or unhealthy.

- **Machine Learning Integration:**  
  The system employs active learning, meaning it refines its model based on user-provided labels.

---

## Features

- **Backend:** Flask/Redis (Python), Keras/TensorFlow Modeling  
- **Frontend:** HTML5 + Jinja2 Flask Templates, JavaScript (Fetch API)

---

## Technologies Used

- Flask (backend server)
- JavaScript Fetch API (client-server communication)
- HTML5/CSS (UI)
- Keras/TensorFlow (classification)

---

## Getting Started

### Requirements

- Python **3.9.11**  
  *(Newest Python version with Keras/TensorFlow support as of 5/9/25)*

---

### 1. Clone the repository

```bash
git clone https://github.com/alan-r03/agro-ai.git
````

---

### 2. Static Files Setup

* Create a `/static` directory inside `/app` if not already present:
  `/app/static`
* Download, unzip, and place **all images** into:
  `/app/static/imgHandheld`
* Download, unzip, and place **imgAnnotations.csv** into:
  `/app/static`
* Files can be found here:
  [Download Link](https://unomail-my.sharepoint.com/:f:/g/personal/alanramirez_unomaha_edu/EpaXuPd3h55HmHWkGkiRuI4BT69kCWVeY8orjI3qdcaY_w?e=ytg8tf)

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Redis Setup

### Windows

1. Install **Windows Subsystem for Linux (WSL)**:

   ```bash
   wsl --install
   ```
2. Open WSL terminal and complete initial setup.
3. Run the following to start Redis:

   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo service redis-server start
   ```
4. Verify Redis is running:

   ```bash
   redis-cli ping
   ```
5. **Subsequent starts:**

   ```bash
   sudo service redis-server start
   ```

---

### MacOS

1. Install Redis:

   ```bash
   brew install redis
   brew services start redis
   ```
2. Verify Redis is running:

   ```bash
   redis-cli ping
   ```
3. **Subsequent starts:**

   ```bash
   brew services start redis
   ```

---

## Run the Application

1. Ensure Redis server is running.
2. Execute:

   ```bash
   python runApp.py
   ```
3. Open a browser and go to:

   ```
   http://127.0.0.1:5000
   ```
