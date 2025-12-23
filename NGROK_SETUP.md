# ngrok Setup Guide

## ทำไมต้อง comment ngrok ออก?

ngrok ต้องการ **authtoken** เพื่อทำงาน หากไม่มี authtoken container จะ restart วนๆ และทำให้เกิด error

## วิธีเปิดใช้งาน ngrok (เมื่อต้องการ public webhooks)

### 1. สมัครและรับ authtoken
1. ไปที่ https://dashboard.ngrok.com/signup
2. สมัครสมาชิก (ฟรี)
3. ไปที่ https://dashboard.ngrok.com/get-started/your-authtoken
4. Copy authtoken ของคุณ

### 2. สร้างไฟล์ ngrok.yml
สร้างไฟล์ `ngrok.yml` ในโฟลเดอร์โปรเจค:

```yaml
version: "2"
authtoken: YOUR_NGROK_AUTH_TOKEN_HERE

tunnels:
  n8n:
    proto: http
    addr: n8n:5678
    inspect: true
```

**แทนที่ `YOUR_NGROK_AUTH_TOKEN_HERE` ด้วย authtoken จริงของคุณ**

### 3. เปิด uncomment ใน docker-compose.yml
ไปที่ไฟล์ `docker-compose.yml` และเอา `#` ออกจาก ngrok service:

```yaml
  ngrok:
    image: ngrok/ngrok:latest
    container_name: the_one_v4_ngrok
    command:
      - "start"
      - "--all"
      - "--config"
      - "/etc/ngrok.yml"
    volumes:
      - ./ngrok.yml:/etc/ngrok.yml
    ports:
      - "4041:4040"
    depends_on:
      - n8n
    restart: unless-stopped
    networks:
      - the_one_network
```

### 4. Restart Docker Compose
```bash
docker-compose down
docker-compose up -d
```

### 5. เข้าถึง ngrok dashboard
- เปิด http://localhost:4041
- จะเห็น public URL สำหรับ n8n webhooks

## สำหรับการพัฒนา Local
**ไม่จำเป็นต้องใช้ ngrok!** 
- n8n ทำงานได้ปกติที่ http://localhost:5679
- ใช้ webhook ภายใน network ได้เลย
- ngrok จำเป็นเฉพาะเมื่อต้องการให้ระบบภายนอก (เช่น LINE, Facebook) เรียก webhook

## ⚠️ คำเตือน
- **อย่า commit ไฟล์ `ngrok.yml`** ที่มี authtoken เข้า git
- เพิ่ม `ngrok.yml` ใน `.gitignore`
