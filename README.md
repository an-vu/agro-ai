# Agro-AI

## CSCI 4970 Capstone Project

This project aims to build trust among farmers in artificial intelligence by demonstrating an interactive learning system. Users will provide input to a machine learning algorithm and observe how their feedback impacts its accuracy.

## Project Overview

- **Core Functionality**: Users will interact with a web-based interface to label images of corn as either *healthy* or *unhealthy*.  
- **Machine Learning Integration**: The system employs *active learning*, meaning it refines its model based on user-provided labels.  

## Features

- **Backend**: Flask/Redis (Python), Keras/Tensorflow Modeling
- **Frontend**: HTML5+Jinja2 Flask Templates, JavaScript (Fetch API)  

## Technologies Used

- Flask (for the backend server)  
- JavaScript Fetch API (for client-server communication)  
- HTML5/CSS (for UI)  
- Keras/Tensorflow (for classification)

## Getting Started

Ensure you are running on Python 3.9.11- this is the newest version available with support for Keras/Tensorflow, as of 5/9/25

Clone this repository:

```sh
git clone https://github.com/alan-r03/agro-ai.git
```

pip install requirements.txt

After cloning, set up redis. Redis manages much of the user's web information.

## Redis setup (Windows)
1. install the Windows Subsystem for Linux (WSL)
^ first, open a powershell or cmd terminal as an administrator, and run the following command
*wsl --install*
2. open the wsl terminal and complete the initial setup
3. run the following commands to initialize the redis server
*sudo apt update*
*sudo apt install redis-server*
*sudo service redis-server start*
to verify the redis-server is live, run the following on the WSL terminal:
*redis-cli ping*

## After first setup of the redis server on Windows, only the following is required to start
1. open a terminal and run the following commands,
*sudo service redis-server start*

## Redis setup (MacOS)

1. pip install requirements.txt
2. open a terminal and run the following commands,
*brew install redis*
*brew services start redis*
*redis-cli ping* **optional: this will verify that the redis server is up and running**

## After first setup of the redis server on MAC, only the following is required to start
1. open a terminal and run the following commands,
*brew services start redis*

Once the redis server is running and the packages are installed, execute 'runApp.py'.

In a web browser, navigate to 127.0.0.1:5000 to open the Agro-AI website.