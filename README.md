<<<<<<< HEAD
# ecommerce-backend-api
Back-end API'S For E-commerce App Project Given By Bheema Info-tech 
=======
# 🛒 E-Commerce Backend API

A production-ready backend API for an e-commerce platform built using **Django, Django REST Framework, PostgreSQL, and JWT Authentication**.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- JWT-based authentication (access & refresh tokens)
- Role-Based Access Control (Admin, Seller, Customer)
- Secure permissions using custom DRF permission classes

### 📦 Product Management
- Product & category management
- Seller-based ownership control
- Search, filtering, sorting & pagination
- Soft delete for data integrity

### 🛒 Cart System
- Persistent user cart
- Add/update/remove items
- Stock validation
- Dynamic price calculation

### 📄 Order Management
- Convert cart to order
- Atomic transactions for stock safety
- Order status tracking

### 💳 Payment Integration
- Razorpay payment gateway (Test Mode)
- Secure payment signature verification
- Order marked as PAID after verification

### ⚡ Performance Optimization
- Query optimization using select_related & prefetch_related
- Database indexing
- Server-side pagination
- ~40% improvement in response times

### 🧠 Database & Security
- PostgreSQL with constraints & JSONField
- API throttling
- Centralized exception handling
- Environment-based configuration

### 📘 API Documentation
- Swagger / OpenAPI documentation
- Interactive API testing

---

## 🧰 Tech Stack

- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Authentication: JWT (SimpleJWT)
- Payments: Razorpay (Test Mode)
- Documentation: drf-spectacular (Swagger)
- Tools: Git, Postman

---

## ▶️ Setup Instructions

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
cd config
python manage.py runserver
>>>>>>> 809afe0 (Initial commit: Django ecommerce backend API)
