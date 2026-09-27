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

### 3. Configure environment

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API root: http://localhost:8000
- GraphQL playground: http://localhost:8000/graphql
- Swagger docs: http://localhost:8000/docs

## Example GraphQL Queries

### Create a category and product

```graphql
mutation {
  createCategory(input: { name: "Electronics", description: "Electronic items" }) {
    id
    name
  }
}

mutation {
  createProduct(input: {
    sku: "LAP-001"
    name: "Laptop"
    unitPrice: "999.99"
    categoryId: 1
  }) {
    id
    sku
    name
  }
}
```

### Record stock inbound

```graphql
mutation {
  createWarehouse(input: { name: "Main Warehouse", location: "Building A" }) {
    id
    name
  }

  setInventory(input: {
    productId: 1
    warehouseId: 1
    quantity: 100
    reorderLevel: 20
  }) {
    quantity
    reorderLevel
  }

  recordStockMovement(input: {
    productId: 1
    warehouseId: 1
    movementType: IN
    quantity: 50
    reference: "PO-001"
  }) {
    id
    movementType
    quantity
  }
}
```

### Query low stock

```graphql
query {
  lowStock {
    quantity
    reorderLevel
    product { name sku }
    warehouse { name }
  }
}
```

## License

MIT
