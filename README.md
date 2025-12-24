# Call & Session Service (FastAPI + LiveKit)

Service ini bertanggung jawab untuk **manajemen call dan session** menggunakan REST API, dengan integrasi **LiveKit** untuk real-time audio/video. Arsitektur dirancang **idempotent**, **event-driven**, dan **production-ready**.

---

## 📐 High-Level Architecture

→ FastAPI Backend
→ PostgreSQL
→ LiveKit Server

---

## ✨ Features

- REST API for call and session management
- LiveKit token generation (room-based)
- Idempotent `end_call`
- LiveKit webhook listener
- SQLAlchemy + Repository Pattern
- Alembic migrations
- Input validation (Pydantic)
- Consistent error handling
- Logging & observability
- Swagger docs at `/docs`
- CORS & Authorization middleware
- Health check endpoints
- Maintain requirements.txt (service-level) and requirements-common.txt

---

## 📦 Project Structure

```
backend/
├── main.py # FastAPI app entrypoint
├── deps.py # Dependency injection (DB, auth, etc)
├── error.py # Custom error definitions
├── logging.py # setup logging
│
├── api/
│ ├── calls.py # Call & session REST API
│ └── webhooks.py # LiveKit webhook listener
│
├── middlewares/
│ ├── auth.py # Authorization middleware
│ └── logging.py # Logging Middleware
│
├── schemas/
│ └── call.py # Pydantic request/response models
│
├── services/
│ ├── call_service.py # Call & session business logic
│ └── livekit_service.py # LiveKit token & room management
│
├── database/
│ ├── engine.py # SQLAlchemy engine & session
│ │
│ ├── alembic/
│ │ ├── env.py
│ │ └── versions/ # Alembic migrations
│ │
│ ├── models/
│ │ ├── init.py
│ │ ├── call.py # Call ORM model
│ │ ├── session.py # Session ORM model
│ │ └── user.py # Session ORM user
│ │
│ └── repositories/
│   ├── base.py
│   ├── call_repo.py # Call repository
│   ├── session_repo.py # Session repository
│   └── user_repo.py # User repository
│
├── requirements.txt # Service-level dependencies
├── requirements-common.txt # Shared dependencies
└── setup.py # Packaging & installation
```

---

## 🚀 API Endpoints

### 1️⃣ Start Call

**POST** `/calls`

Create call dan initial session.

```json
{
  "caller_id": "user_a"
}
```

Response 

```json
{
  "call_id": "uuid",
  "caller_id": "user_a",
  "session_id": "uuid",
  "started_at": "ISO8601",
  "ended_at": null,
  "livekit_token": "jwt",
  "room_name": "call_<call_id>"
}
```

📌 Frontend

- Setelah mendapatkan token, Frontend langsung join LiveKit
- Tidak lewat backend lagi

---

### 2️⃣ Join Call

**POST** `/calls/{call_id}/join/{user_id}`

```json
{
  "call_id": "uuid",
  "session_id": "uuid",
  "livekit_token": "jwt",
  "room_name": "call_<call_id>"
}
```

---

### 3️⃣ End Call (Idempotent)

**POST** `/calls/{call_id}/end`

Behavior:

- Call aktif → end call + end semua session
- Call sudah ended → no-op
- Aman dipanggil berulang
- Room LiveKit dihapus

**🔁 Idempotency Strategy**

- Idempotency berbasis state, bukan Idempotency-Key.
- ended_at != null → request diabaikan
- Tidak ada circular flow dengan webhook

---

### 🔔 LiveKit Webhook

**POST** `/webhooks/livekit`

Handled events:

- participant_joined
- participant_left
- room_finished

Tujuan:

- Sinkronisasi state backend
- Fallback jika client disconnect
- Tidak memicu /calls/end langsung

---

### 🩺 Health Check

**GET** `/health`
```json
{
  "status": "ok"
}
```

---

## 🧱 Middleware
- CORS
- Authorization
- Webhook Authorization
- Logger

---

## 🗄️ Database & Migration

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

---

## 🔐 Environment Variables
```env
DATABASE_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
LIVEKIT_URL=
LIVEKIT_WEBHOOK_SECRET=
```