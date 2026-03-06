# 🏥 HospitaKr Enterprise Pro
### Developed by Md Noaman (Noa)

Welcome to **HospitaKr Enterprise Pro**, a high-performance Hospital Management System I built to explore modern GUI development and local database management. This application focuses on providing a clean, dark-themed experience for healthcare administrators to manage patient data and clinical records efficiently.

---

## 🚀 Why I Built This
I wanted to create a desktop solution that wasn't just functional, but also visually modern. Moving away from standard Tkinter, I utilized **CustomTkinter** to achieve a "SaaS-style" look and integrated **ReportLab** to handle real-world needs like automated medical PDF generation.

---

## ✨ Core Features
* **🔐 Admin Gatekeeper:** A secure Login/Signup system to protect sensitive patient data.
* **📊 Live Insights:** A dynamic dashboard that calculates total revenue, patient count, and staff capacity on the fly.
* **👥 Full Patient Lifecycle:** From check-in to discharge, manage patient IDs, room assignments, and billing.
* **👨‍⚕️ Medical Directory:** Specialized views for doctors (with specialty tracking) and general hospital staff.
* **📄 One-Click Reporting:** Instantly generate professional medical PDF summaries for any patient ID.
* **🎨 Dark Mode UI:** Built with a focus on "Inter" typography and a professional #0F172A color palette.

---

## 🛠️ My Tech Stack
* **Python 3.x** - The backbone of the logic.
* **CustomTkinter** - For the modern, responsive UI.
* **SQLite3** - For lightweight, local database storage.
* **ReportLab** - To handle the automated PDF document generation.

---

## 📂 Project Structure
* `app.py` - The main application engine.
* `hospita_pro_v4.db` - The local database (automatically initialized on first run).
* `Detailed_Medical_Record_*.pdf` - Format for generated clinical reports.

----

## ⚙️ How to Run My Project

### 1. Grab the Dependencies
You'll need to install the libraries I used:
```bash
pip install customtkinter reportlab
