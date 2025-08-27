# DIMA WMS – Technical Test Submission

This repository contains my solution for **Remote Software Engineer: Technical Test 01 – Inventory Management**.
The project consists of **two microservices**:

* **MSInventory** → Django REST Framework + PostgreSQL backend
* **MSWebclient** → Vue.js + TypeScript frontend

Both services implement inventory features for **DIMA WMS**, including CRUD operations, stock moves, multi-product support, and real-time inventory tracking.

---

## ⚙️ Prerequisites

Ensure the following are installed:

* **Python 3.10+**
* **Node.js v18+** & **npm**
* **PostgreSQL 12.0+**
* **Git**

---

# 🖥 Backend – MSInventory

The backend is built with **Django REST Framework**, handles inventory operations, and exposes **JWT-protected API endpoints**.
Swagger documentation is available for testing all endpoints.

---

### 1. Environment Variables

Create a `.env` file in `msinventory/`:

```
DEBUG=True
SECRET_KEY=QWESWESDSD1223EQDEF
DB_NAME=dima
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

### 2. Database Setup

```bash
# Create database
createdb -U postgres dima

# Or using psql:
psql -U postgres -c "CREATE DATABASE dima;"

# Optional: restore dump 
psql -U postgres -d dima < dump/dima.sql
```

---

### 3. Backend Setup & Commands

```bash
# Navigate to backend
cd msinventory

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (if not auto-created)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

> Backend available at **[http://localhost:8000/](http://localhost:8000/)**

> Swagger API docs: **[http://localhost:8000/swagger/](http://localhost:8000/swagger/)**

> Admin panel: **[http://localhost:8000/admin/](http://localhost:8000/admin/)**

**Default Admin Credentials, Created Automatically When Backend Runs:**

```
Username: admin
Password: admin123
```

---

### 4. Backend Features

✅ Products CRUD
✅ Locations CRUD
✅ Stock Moves CRUD (INBOUND, OUTBOUND, TRANSFER)
✅ Stock move with multiple products (optional task)
✅ Real-time Inventory Levels per product/location
✅ JWT authentication
✅ Exception handling & user-friendly messages

---

### 5. Backend Project Structure

```
msinventory/
├── inventory/            # All Django apps
│   ├── locations/
│   ├── products/
│   ├── snapshots/
│   ├── stockmoves/
│   └── suppliers/
├── msinventory/          # Main Django project
├── utils/                # Utility functions (exceptions, helpers, JWT)
├── .env
├── flakes
├── app.yaml
├── load_initial_data.py
├── manage.py
├── README.md
└── requirements.txt

```

*(Each app contains migrations, models, serializers, views, urls, and tests as needed)*

---

# 🌐 Frontend – MSWebclient

The frontend is built with **Vue.js + TypeScript** and communicates with the backend via API.

---

### 1. Environment Variables

Create a `.env` file in `mswebclient/`:

```
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_VERSION=1.20.3
```

---

### 2. Frontend Setup & Commands

```bash
# Navigate to frontend
cd mswebclient

# Install dependencies
npm install

# Start development server
npm run dev

# For production build
npm run build
npm run preview
```

> Frontend available at **[http://localhost:8080/](http://localhost:8080/)**

---

### 3. Frontend Features

✅ CRUD pages for Products, Locations, Suppliers
✅ CRUD & intuitive Stock Move creation (single & multi-product)
✅ Real-time Inventory Level display
✅ Exception handling & user-friendly messages

---

### 4. Frontend Project Structure

```
mswebclient/ 
├── public/
├── src/
│   ├── api/
│   ├── components/
│   │   ├── forms/
│   │   └── layout/
│   ├── pages/
│   ├── router/
│   ├── store/
│   ├── types/
│   ├── utils/
│   ├── App.vue
│   ├── main.js
│   └── shims-vue.d.js
├── style.css
├── texts/
├── env/
├── index.html
├── package-lock.json
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── jsconfig.json
└── vite.config.js
```

*(src/components/forms contains form components; src/pages contains page components for CRUD operations)*

---

## 🔑 Authentication

* JWT-protected backend endpoints
* Obtain token via:

```http

  "username": "admin",
  "password": "admin123"

```


---

## 📝 Additional Useful Commands

```bash
# Backend tests
python manage.py test

# Create new migrations after model changes
python manage.py makemigrations

```

---

## 🖥 Access Points

* **Backend API**: [http://localhost:8000](http://localhost:8000)
* **Frontend App**: [http://localhost:8080](http://localhost:8080)
* **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)
* **API Documentation (Swagger)**: [http://localhost:8000/swagger](http://localhost:8000/swagger)

> The backend must be running before the frontend can make successful API calls. Both servers can run simultaneously on different ports.

---

## 👤 Author

**\[Temban Blaise Ayim]**
📧 \[[tembanblaise12@gmail.com](mailto:tembanblaise12@gmail.com)]

---




<img width="992" height="822" alt="Screenshot 2025-08-27 031732" src="https://github.com/user-attachments/assets/c003e506-8b8d-4235-a223-106e8446f8bc" />

<img width="1248" height="585" alt="Screenshot 2025-08-27 031655" src="https://github.com/user-attachments/assets/0f1a3f0e-bdd4-4908-923b-817cec3103a4" />

<img width="1272" height="890" alt="Screenshot 2025-08-27 031754" src="https://github.com/user-attachments/assets/57120545-0bbd-4a3d-aa47-b93b04b2d568" />

<img width="1267" height="882" alt="Screenshot 2025-08-27 031808" src="https://github.com/user-attachments/assets/74bdb943-b716-4c53-b2be-5fca386b91b2" />

<img width="983" height="923" alt="Screenshot 2025-08-27 031838" src="https://github.com/user-attachments/assets/488d6059-631f-4ca0-b48f-a15c38c486df" />

<img width="1250" height="650" alt="Screenshot 2025-08-27 031906" src="https://github.com/user-attachments/assets/e1d7e0c9-7d61-4b53-ac9d-b0e99a7f4f65" />

<img width="1287" height="842" alt="Screenshot 2025-08-27 031931" src="https://github.com/user-attachments/assets/dce11e68-1a0b-461a-89c9-225d0abeb29c" />

<img width="1284" height="799" alt="Screenshot 2025-08-27 031942" src="https://github.com/user-attachments/assets/8ba7dadf-a030-4a1d-be72-d4220472f4d9" />

<img width="1250" height="500" alt="Screenshot 2025-08-27 032007" src="https://github.com/user-attachments/assets/02f96061-812c-44b6-a0a0-4667ed886b1b" />

<img width="1251" height="780" alt="Screenshot 2025-08-27 032024" src="https://github.com/user-attachments/assets/ca3e9641-d608-486b-9f85-933c19d041b3" />

<img width="1019" height="922" alt="Screenshot 2025-08-27 032220" src="https://github.com/user-attachments/assets/330e9b3c-1f9d-4bcc-9305-04bed2a56f9f" />

<img width="995" height="936" alt="Screenshot 2025-08-27 032237" src="https://github.com/user-attachments/assets/c4c3513e-0078-4dda-b7cb-1818a81305d6" />

<img width="1026" height="931" alt="Screenshot 2025-08-27 032256" src="https://github.com/user-attachments/assets/03e13234-5b88-4157-9656-7ad6196855f9" />

<img width="1020" height="443" alt="Screenshot 2025-08-27 032321" src="https://github.com/user-attachments/assets/4c72d7e2-5d36-439f-bf86-7787c4b88424" />

<img width="1014" height="531" alt="Screenshot 2025-08-27 032346" src="https://github.com/user-attachments/assets/eceedd53-81b1-4e7d-80a6-6b5254ebcaba" />

<img width="1261" height="810" alt="Screenshot 2025-08-27 035135" src="https://github.com/user-attachments/assets/f7a59044-be38-4dab-a03b-f17ed52f823f" />

<img width="1260" height="519" alt="Screenshot 2025-08-27 032431" src="https://github.com/user-attachments/assets/064343b3-6f4a-41d4-8391-8e9081df65a1" />

<img width="758" height="1767" alt="Screenshot 2025-08-27 032846" src="https://github.com/user-attachments/assets/e99b224c-f852-4fd0-82a3-ae4698cf721c" />









