# 🚗 Aman Drive -Vehicle Crash Detection-

This is the backend API for **Aman Drive**, a vehicle crash detection application. It receives audio input, processes it using a deep learning model, and classifies whether a car crash event is detected.

## 🛠️ Technologies Used

- Python 3.8+
- Flask
- TensorFlow / Keras (for the prediction model)
- Librosa / NumPy (for audio processing)
- Docker

## 📬 API Endpoints

### Client

| Method | Endpoint       | Description                |
|--------|---------------|----------------------------|
| POST   | `/login`      | Login user and get a token  |
| POST   | `/predict`    | Get prediction of vehicule's audio (safe/crash) |
| GET    | `/users/<int:user_id>` | Get user information (profile) |

---

### Police

| Method | Endpoint       | Description                |
|--------|---------------|----------------------------|
| POST   | `/login`      | Login user and get a token  |
| GET    | `/users/<int:user_id>` | Get user information (profile) |
| GET    | `/police/accidents`  | Get accidents handled by the police station |

---

### Insurance

| Method | Endpoint       | Description                |
|--------|---------------|----------------------------|
| POST   | `/login`      | Login user and get a token  |
| GET    | `/users/<int:user_id>` | Get user information (profile) |
| GET    | `/clients`  | Get all clients of the insurance company |
| POST   | `/clients`  | Create new client for the insurance company |
| PUT    | `/clients/<int:client_id>`  | Update a client's information |
| DELETE | `/clients/<int:client_id>`  | Delete a client |

---

### Admin

| Method | Endpoint       | Description                |
|--------|---------------|----------------------------|
| POST   | `/login`      | Login user and get a token  |
| GET    | `/users/<int:user_id>` | Get user information (profile) |
| GET    | `/users` | Get all users |
| GET    | `/accidents` | Get all accidents |
| GET    | `/insurances`  | Get all insurance companies |
| POST   | `/insurances`  | Create new insurance company |
| PUT    | `/insurances/<int:client_id>`  | Update an insurance company's information |
| DELETE | `/insurances/<int:client_id>`  | Delete an insurance company |
| GET    | `/police`  | Get all police stations |
| POST   | `/police`  | Create new police station |
| PUT    | `/police/<int:client_id>`  | Update an police station's information |
| DELETE | `/police/<int:client_id>`  | Delete an police station |

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/lyna555/aman-drive.git
cd aman-drive
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Flask app

```bash
python app.py
```
By default, the app runs on http://127.0.0.1:5000.

## ⚙️ Environment Variables
```bash
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
SECRET_KEY=your_jwt_secret_key
```

## 📦 Docker (Optional)
```bash
docker build -t aman-drive:1.0
docker run -d -p 5000:5000 aman-drive:1.0
```



