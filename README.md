## e-card-app-v2
This is flask and Vue based dummy project created for App Dev II project sessions for May 2025. 

## Prerequisites

Make sure the following are installed on your system:

- [Python 3.8+](https://www.python.org/downloads/windows/)
- [Git](https://git-scm.com/downloads)
- A code editor like [VS Code](https://code.visualstudio.com/)

## Setup Instructions

Follow the steps below to fork, clone, and run this project on your local Windows system. You can follow the same process for your own project.

### 1. Fork the Repository

Click the **Fork** button at the top-right corner of this repository on GitHub to create your own copy.

### 2. Clone the Repository

Open Git Bash or Command Prompt and run:

```bash
git clone https://github.com/YOUR-USERNAME/e-card-app-v2.git
cd e-card-app-v2
```
## A. Backend setup

### 1. Create and Activate a Virtual Environment 

```bash
Run the following commands in your backend directory inside the project directory:
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate
```
You should see (venv) in your terminal indicating that the virtual environment is active.

### 2. Install Dependencies

```bash
pip freeze > requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

Open your browser and go to `http://127.0.0.1:5000/` to see the app running.

## B. Frontend setup

This guide walks you through setting up a Vue 3 project using [Vite](https://vitejs.dev/), configuring it properly, and installing commonly used packages.

### 1. Ensure the following tools are installed on your machine:

- [Node.js (v16+ recommended)](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

You can verify installations using:

```bash
node -v
npm -v
```

### 2. Create a New Vite + Vue 3 Project

```bash
npm create vite@latest
```

1. Name your project `Frontend`.
2. Select `vue` as framework.
3. Select `javaScript` as programming language.

### 3. Change directory

```bash
cd Frontend
```

### 4. Install dependencies

Install required packages (inside project folder)

```bash
npm install
```

### 5. Install Axios (for API calls)

```bash
npm install axios
```

### 6. Run the development server

```bash
npm run dev
```

## Note
This README.md will be updated as the project develops. Please check back periodically for new setup instructions, features, and improvements.