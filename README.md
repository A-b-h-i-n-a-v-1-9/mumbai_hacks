Scamp is an **AI‑powered security assistant** that detects deepfake scams in images, audio, text, and web pages.  
It works across **Telegram**, a **Chrome extension**, and a **REST backend**, and can also generate **PDF cybercrime reports**.

This repository contains:
- The **backend** (FastAPI + ML detectors)
- The **Telegram bot**

- The **Chrome extension**
    
- The **landing website**
    
- Utility scripts & notebooks
    

---

## 🚀 Features

### **1. Real‑time Scam Detection (Image, Text)**

- Detects deepfake patterns
    
- Flags fraud signals (KYC scams, OTP requests, fake payment links, impersonation)
    
- Generates **risk scores (0–100)**: Low / Medium / High
    
- Works inside Telegram or via API
    

### **2. Explainability**

- Shows _why_ something is risky
    
- Gives highlight signals:
    
    - “KYC link”
        
    - “OTP request”
        
    - “Suspicious banking phrase”
        
    - “Voice inconsistency”
        

### **3. PDF Cybercrime Reports**

- Auto‑generated professional PDF
    
- Includes event details, timestamps, risk interpretation
    
- Helps users file cybercrime complaints quickly
    

### **4. Chrome Extension**

- Scan selected text
    
- Scan the entire webpage using live extraction
    
- Sends data to backend & shows scam risk
    
- Supports OCR + text scraping (content script)
    

### **5. Website / Landing Page**

- Modern product site for Scamp
    
- Explains features, pricing, and use cases
    
- CTA links to the Telegram bot

## 📂 Repository Structure

mumbai_hacks/
│
├── scamp/                 # Backend + Bot + Reports
│   ├── backend/           # FastAPI service
│   ├── bot/               # Telegram bot
│   ├── uploads/           # Media uploads
│   ├── reports/           # PDF reports generated
│   └── dashboard/         # (optional future)
│
├── scamp_website/         # Product landing page
│
└── ChromeExtension/       # Browser extension source

## 🧠 Backend (FastAPI)

### **Key routes**

- `POST /analyze` → analyze images/audio
    
- `POST /analyze_text` → analyze text
    
- `GET /report/{event_id}` → return PDF report
    
- `GET /ping` → health check
    

### **Tech**

- FastAPI
    
- python‑multipart
    
- reportlab
    
- SQLite (events DB)
    
- ML-based detectors
    

---

## 🤖 Telegram Bot

**Features:**

- Auto‑scan any text, image, audio
    
- Sends risk level message + highlight explanation
    
- Buttons for:
    
    - Block payment (simulated)
        
    - Mark safe
        
    - Generate report (inline or PDF)
        
- Smooth UX with async file downloading
    

Run:

`python bot/bot.py`

Environment variables:

`export BACKEND_URL="http://127.0.0.1:8000" export TELEGRAM_BOT_TOKEN="your-token"`

---

## 🧩 Chrome Extension

**Capabilities:**

- “Scan Selection” → analyze highlighted text
    
- “Scan Full Page” → extract visible text + run analysis
    
- Sends results to backend
    
- Works on any site
    

Includes:

- manifest.json
    
- popup.html / popup.js
    
- content.js (for full-page scanning)
    

Load via:  
Chrome → Extensions → Developer Mode → Load Unpacked

---

## 🌐 Website

Located in `/scamp_website/`

Features:

- Hero section
    
- Features grid
    
- Pricing section
    
- Testimonials
    
- CTA links to Telegram bot
    
- Styled with dark fintech UI + glassmorphism
    

---

## 📄 PDF Report Generation

Uses `reportlab` to create:

- Scam details
    
- Metadata
    
- Score interpretation
    
- Safety recommendations
    
- Timestamp
    

Triggered via:

- Telegram bot (“Generate Report”)
    
- GET `/report/{event_id}`
    

---

## 🛠 Setup Instructions

### 1. Create virtual environment

python -m venv env
source env/bin/activate       # Mac/Linux
env\Scripts\activate          # Windows

### 2. Install dependencies

`pip install -r requirements.txt`

### 3. Run backend

`uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000`

### 4. Run Telegram bot

`python bot/bot.py`

### 5. Load Chrome extension

Chrome → Extensions → Load Unpacked → select `ChromeExtension/`

---

## 🧪 Testing

Use:

- `/test_images`
    
- Sample scam text
    
- Chrome extension
    
- Telegram bot chats
    

---

## 📦 Future Roadmap

- WhatsApp integration
    
- Browser‑side ML checks
    
- Premium + business dashboards
    
- Multi-language detection
    
- Device-side scanning
    

---

## 📞 Contact

For queries or contributions:  
**Team Scamp**  
Telegram bot: https://web.telegram.org/k/#@scamp_security_bot
