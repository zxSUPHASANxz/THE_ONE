# THE ONE - Quick Start Guide

## 📋 สิ่งที่ต้องเตรียม

1. Python 3.11 ขึ้นไป ✅
2. Docker Desktop
3. Node.js 18+ (สำหรับ TailwindCSS)
4. PostgreSQL (หรือใช้ Docker)
5. ngrok account (optional)

## 🚀 การติดตั้งและรันโปรเจค

### 1. ติดตั้ง Dependencies

```bash
# ติดตั้ง Python packages (ทำแล้ว ✅)
.\venv\Scripts\activate
pip install -r requirements.txt

# ติดตั้ง Node.js packages สำหรับ TailwindCSS
npm install
```

### 2. ตั้งค่า Environment Variables

แก้ไขไฟล์ `.env` ตามความต้องการ (มีไฟล์ `.env` แล้ว ✅)

### 3. เริ่มต้น Docker Services

```bash
# เริ่ม PostgreSQL และ n8n
docker-compose up -d

# ตรวจสอบสถานะ
docker-compose ps
```

### 4. รัน Migrations

```bash
# สร้าง database schema
.\venv\Scripts\python.exe manage.py migrate

# สร้าง superuser สำหรับ Django admin
.\venv\Scripts\python.exe manage.py createsuperuser
```

### 5. Build TailwindCSS

```bash
# Build CSS (first time)
npm run tailwind:build

# หรือ watch mode สำหรับ development
npm run tailwind:watch
```

### 6. รัน Development Server

```bash
# เปิด terminal ใหม่สำหรับ Django server
.\venv\Scripts\activate
.\venv\Scripts\python.exe manage.py runserver
```

## 🔗 URL ที่สำคัญ

- Django Application: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- n8n Workflow: http://localhost:5678 (user: admin, pass: admin)
- ngrok Dashboard: http://localhost:4040
- PostgreSQL: localhost:5432

## 📱 API Endpoints

### Authentication
- POST `/api/users/register/` - สมัครสมาชิก
- POST `/api/users/token/` - Login (รับ JWT token)
- POST `/api/users/token/refresh/` - Refresh token
- GET/PUT `/api/users/profile/` - ดูและแก้ไขโปรไฟล์

### Chatbot
- GET/POST `/api/chatbot/sessions/` - จัดการเซสชันแชท
- GET `/api/chatbot/sessions/<session_id>/` - ดูเซสชันเฉพาะ
- POST `/api/chatbot/messages/` - ส่งข้อความ
- POST `/api/chatbot/webhook/` - n8n webhook
- GET `/api/chatbot/knowledge/` - ค้นหาความรู้

### Booking
- GET/POST `/api/booking/motorcycles/` - จัดการรถของคุณ
- GET/PUT/DELETE `/api/booking/motorcycles/<id>/` - รายละเอียดรถ
- GET/POST `/api/booking/bookings/` - จัดการการจอง
- GET/PUT `/api/booking/bookings/<id>/` - รายละเอียดการจอง
- POST `/api/booking/bookings/<id>/cancel/` - ยกเลิกการจอง

### Mechanics
- GET/PUT `/api/mechanics/profile/` - โปรไฟล์ช่าง
- GET `/api/mechanics/queue/` - คิวงานช่าง
- POST `/api/mechanics/queue/<id>/accept/` - รับงาน
- POST `/api/mechanics/queue/<id>/reject/` - ปฏิเสธงาน
- GET `/api/mechanics/reviews/` - รีวิวช่าง
- POST `/api/mechanics/reviews/create/` - สร้างรีวิว

## 🐳 Docker Commands

```bash
# เริ่มต้น services
docker-compose up -d

# หยุด services
docker-compose down

# ดู logs
docker-compose logs -f

# ดู logs เฉพาะ service
docker-compose logs -f n8n
docker-compose logs -f postgres

# Restart service
docker-compose restart n8n
```

## 🛠️ n8n Configuration

1. เข้า http://localhost:5678
2. Login ด้วย admin/admin
3. สร้าง workflow สำหรับ:
   - รับข้อความจาก Django webhook
   - ทำ web scraping (Pantip, เว็บไซต์รถ)
   - ทำ RAG (Retrieval-Augmented Generation)
   - ส่งผลลัพธ์กลับไปที่ Django

### ตัวอย่าง n8n Workflow

**Node 1: Webhook** (รับข้อมูลจาก Django)
- Method: POST
- Path: /webhook/chat

**Node 2: HTTP Request** (ค้นหาข้อมูลจาก external sources)
- URL: Pantip API หรือเว็บไซต์อื่น
- Method: GET

**Node 3: AI Processing** (ประมวลผลด้วย RAG)
- ใช้ OpenAI API หรือ Local LLM

**Node 4: HTTP Request** (ส่งกลับไปที่ Django)
- URL: http://host.docker.internal:8000/api/chatbot/webhook/
- Method: POST

## 🔧 การแก้ไขปัญหา

### PostgreSQL Connection Error
```bash
# ตรวจสอบว่า PostgreSQL ทำงานหรือไม่
docker-compose ps

# Reset database
docker-compose down -v
docker-compose up -d
.\venv\Scripts\python.exe manage.py migrate
```

### n8n Not Working
```bash
# Restart n8n
docker-compose restart n8n

# Check logs
docker-compose logs -f n8n
```

### TailwindCSS Not Building
```bash
# ลบและติดตั้งใหม่
rm -rf node_modules
npm install
npm run tailwind:build
```

## 📝 Next Steps

1. ✅ โครงสร้างโปรเจคสร้างเสร็จแล้ว
2. ⏳ ต้องรัน Docker และ Migrations
3. ⏳ ต้องสร้าง n8n workflows
4. ⏳ ต้อง build TailwindCSS
5. ⏳ ต้องทดสอบระบบ

## 📞 Support

หากมีปัญหาใดๆ โปรดตรวจสอบ logs:
- Django: ใน terminal ที่รัน runserver
- n8n: `docker-compose logs -f n8n`
- PostgreSQL: `docker-compose logs -f postgres`
