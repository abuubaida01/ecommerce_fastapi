# E-Commerce Backend (FastAPI)

A high-performance, modular **E-Commerce backend** built using **FastAPI**, designed to support scalable online stores with asynchronous APIs, MySQL integration, and modular architecture for key business domains like **products**, **cart**, **orders**, **payments**, and **shipping**.

---

## Features

### Core Modules
| Module | Description |
|--------|--------------|
| **Account** | Handles user registration, authentication (JWT), profile management, and admin controls. |
| **Product** | Manages product listings, categories, images, and availability. |
| **Cart** | Supports add-to-cart, remove-from-cart, and dynamic price calculations. |
| **Order** | Manages order creation, status tracking, and order history. |
| **Payment** | Handles payment workflows and integrations with third-party payment gateways. |
| **Shipping** | Calculates shipping rates, manages addresses, and updates delivery statuses. |
| **Media** | Stores and serves product and user-uploaded media. |
| **Alembic** | Handles database migrations and schema versioning. |
| **DB** | Contains database models and connection utilities. |

---

## Tech Stack

| Category | Technology |
|-----------|-------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Database** | MySQL |
| **ORM / Migrations** | SQLAlchemy + Alembic |
| **Authentication** | JWT-based authentication |
