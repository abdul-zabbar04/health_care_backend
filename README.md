
---

### **Backend README (Django API)**
```md
# 🏥 Health Care Platform - Backend (Django)

## 📌 Overview
This is the **backend** of the Health Care platform, built using **Django REST Framework**. It provides **secure APIs for user authentication, doctor listings, appointment booking, and payments**.

## 🛠️ Features
- **Authentication**:
  - **JWT-based login/logout**
  - Email verification using `dj-rest-auth`
  - Role-based authentication (Patient/Doctor/Admin)
- **Patients**:
  - View doctor profiles & availability.
  - Book & pay for appointments via **SSLCommerz**.
  - Leave reviews after consultations.
- **Doctors**:
  - View paid appointments in the dashboard.
  - Complete appointments after meeting patients.
- **Admin**:
  - Approve or reject **doctor verification**.
  - Manage users and appointments.
- **Payments**:
  - Integrated **SSLCommerz** payment gateway.
  - Status updates for successful or failed transactions.

## 🛠️ Tech Stack
- **Backend**: Django, Django REST Framework (DRF)
- **Authentication**: dj-rest-auth, Django Allauth, JWT
- **Database**: PostgreSQL (via Supabase)
- **Payment Gateway**: SSLCommerz
- **Hosting**: Vercel

## 🚀 Setup Instructions
1. Clone the repository:
   ```sh
   git clone <backend-repo-url>
