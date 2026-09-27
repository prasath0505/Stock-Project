# Stock Management System

A layered stock management API built with **FastAPI**, **GraphQL (Strawberry)**, **SQLAlchemy**, and **PostgreSQL**.

## Architecture

```
Client
   ↓
FastAPI / GraphQL API
   ↓
Service Layer
   ↓
DAO / Repository Layer
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

## Modules

| Module | Description |
|--------|-------------|
| **Categories** | Product categorization |
| **Products** | SKU, pricing, and product catalog |
| **Suppliers** | Vendor management |
| **Warehouses** | Storage locations |
| **Inventory** | Stock levels per product/warehouse |
| **Stock Movements** | Inbound, outbound, adjustment, transfer |
| **Purchase Orders** | Supplier orders and receiving |

## Project Structure

```
stock_management/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings
│   ├── database.py          # SQLAlchemy engine & session
│   ├── models/              # SQLAlchemy ORM models
│   ├── dao/                 # Data access / repository layer
│   ├── services/            # Business logic layer
│   └── graphql/             # GraphQL schema, types, inputs
├── venv/                    # Virtual environment
├── docker-compose.yml       # PostgreSQL container
├── requirements.txt
└── .env.example
```

## Setup

### 1. Create virtual environment

```bash
cd stock_management
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL

```bash
docker compose up -d
```

### 4. Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API root: http://localhost:8000
- GraphQL playground: http://localhost:8000/graphql
- Swagger docs: http://localhost:8000/docs
