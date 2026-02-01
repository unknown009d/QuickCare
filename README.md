# Quick Care

![Loading](quickcareslowlow.gif)

Visit the web app in : [Live Preview](https://druba.in/QuickCare/frontend)

This project uses a **two-tier architecture**:

* **Backend**: Python (Flask) API server
* **Frontend**: Static PWA (HTML / CSS / JS) served via `live-server`

Both servers run **independently** in development and communicate via HTTP.

---

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   ├── uploads/
│   ├── utils/
│   └── venv/
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── data/
│
├── run-dev.ps1
├── run-dev.sh
└── README.md
```

---

## ⚙️ Prerequisites

Make sure the following are installed:

* **Python 3.10+**
* **Node.js (with npm)**
* **PowerShell** (Windows) or **Bash** (Linux/macOS)

Verify:

```bash
python --version
npm --version
```

---

## 🚀 Development Setup (One Command)

### 🟦 Windows (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\run-dev.ps1
```

### 🟩 Linux / macOS / Git Bash / WSL

```bash
chmod +x run-dev.sh
./run-dev.sh
```

---

## 🔧 What the scripts do automatically

### Backend

* Creates Python virtual environment if missing
* Activates `venv`
* Installs dependencies from `requirements.txt`
* Starts the Python server

### Frontend

* Checks if `live-server` is installed
* Installs it globally via npm if missing
* Serves frontend with live reload on a fixed port

---

## 🌐 Development Ports

| Service  | Default                                        |
| -------- | ---------------------------------------------- |
| Backend  | `http://localhost:5000` *(or configured port)* |
| Frontend | `http://localhost:5500`                        |

> ⚠️ Do **not** change the frontend port frequently —
> this can break **PWA service worker scope & caching**.

---

## 🧠 IMPORTANT: Frontend API URL Configuration

Once the **backend server is running**, you **must update the frontend API URL**.

### 📍 File to edit

```
frontend/js/index.js in Line ~118
```

### 🔧 Change this variable:

```js
const url = "http://127.0.0.1:5000";
```

> Replace the ip address with your machine's ip address. Make sure to change the ip address whenever you connect to a different network. If you want to use it as a standalone one keep it at 127.0.0.1

This is required because:

* Frontend is served separately
* API calls must point to the running backend server

---

## 🔐 CORS & API Communication

* Backend uses **Flask + flask-cors**
* Cross-origin requests from `localhost:5500` are allowed
* No proxy is used (clean tier separation)

---

## 📦 PWA Notes

* `live-server` runs on `localhost`, which is a **secure context**
* Service workers are supported
* If caching behaves unexpectedly:

  ```
  Chrome DevTools → Application → Clear storage → Reload
  ```

---

## ❌ What this setup is NOT

* ❌ No monolithic server
* ❌ No frontend build system
* ❌ No VS Code dependency
* ❌ No backend-served frontend

This is an **explicitly separated dev architecture**.

---

## 🧪 Troubleshooting

### Backend not reachable?

* Confirm backend is running
* Check port number
* Verify `url` in `frontend/js/index.js`

### live-server not found?

```bash
npm install -g live-server
```

### Python packages missing?

```bash
pip install -r backend/requirements.txt
```

---

## 📌 Future Improvements (Optional)

* Auto-restart backend on file change
* Single-port reverse proxy
* Production build & deployment script
* Environment-based config switching

---

## 🏁 Summary

* Two terminals
* Two servers
* Clear separation
* PWA-safe
* Predictable & debuggable

This setup is intentional and optimized for development clarity.