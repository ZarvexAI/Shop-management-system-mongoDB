# ShopKeeper: Shop Management System

A full-stack shop management system for a small shop owner. A **FastAPI + MongoDB** backend keeps products, categories and stock, creates bills, and reduces stock automatically on every sale. A simple **HTML/CSS/JavaScript** frontend sits on top of the API.

## Features

- **Categories:** add, view, update and delete. Names are unique (case-insensitive). Renaming a category also renames it in all its products, and a category that still has products cannot be deleted.
- **Products:** add, view, filter by category, search by name, low-stock list, update, restock and delete. Names are unique, the category must exist, price must be greater than 0 and stock cannot be negative.
- **Sales / billing:** create a bill with several products. Every item is checked first (product exists, enough stock), prices are read from the database (never trusted from the client), and stock is reduced only after the whole bill is valid.
- **Cancel a sale:** the quantities go back to the product stock and the bill is removed.
- **Sales history:** newest first, with search by customer name.
- **Dashboard:** total products, stock value, low-stock count, today's sales count and today's revenue.
- Each bill saves the product name and price at the time of sale, so old bills never change when prices change.

## Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI + Uvicorn | Backend framework and server |
| MongoDB (Atlas or local) | Database |
| PyMongo | MongoDB driver |
| Pydantic | Request validation |
| python-dotenv | Loads the database URI from `.env` |
| Poetry | Dependency management |
| HTML, CSS, JavaScript | Frontend (single file, no build step) |

## Screenshots

| Dashboard | Products |
|---|---|
| ![Dashboard](screenshots/dashboard.png) | ![Products](screenshots/products.png) |

| New sale | Sales history |
|---|---|
| ![New sale](screenshots/new-sale.png) | ![Sales history](screenshots/history.png) |

**Swagger UI**

![Swagger UI](screenshots/swagger.png)

## Project Structure

```
Shop-management-system-mongoDB/
├── main.py                 # FastAPI app, CORS, routers
├── config/
│   └── db_connection.py    # MongoDB connection
├── validations/            # Pydantic models
├── routes/                 # Categories, products, sales, dashboard
├── frontend/
│   └── index.html          # The whole frontend
├── pyproject.toml          # Dependencies (Poetry)
├── poetry.lock
└── .env                    # Not uploaded (contains your DB_URI)
```

## Getting Started

Requirements: Python 3 and [Poetry](https://python-poetry.org/docs/#installation).

### 1. Clone the repository

```
git clone https://github.com/ZarvexAI/Shop-management-system-mongoDB.git
cd Shop-management-system-mongoDB
```

### 2. Install dependencies

Poetry creates the virtual environment and installs the exact versions from `poetry.lock`.

```
poetry install --no-root
```

### 3. Set up the database

Create a `.env` file in the project root:

```
DB_URI=your_mongodb_connection_string
```

Use a free MongoDB Atlas cluster or a local MongoDB (`mongodb://localhost:27017`). The app uses the database `Shop_Management` with three collections: `Categories`, `Products` and `Sales`. They are created automatically on first use.

### 4. Start the backend

```
poetry run uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

### 5. Open the frontend

With the backend running, open `frontend/index.html` in your browser (double-click it). No build step is needed. The API address is set by the `API` constant at the top of the script in that file.

> Create at least one category before adding products, because every product needs an existing category.

## API Endpoints

### Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/Categories/create` | Add a category |
| GET | `/Categories/getall` | List all categories |
| GET | `/Categories/search/{id}` | Get one category by id |
| PUT | `/Categories/update/{id}` | Update a category (also renames it in its products) |
| DELETE | `/Categories/delete/{id}` | Delete a category (blocked if products use it) |

### Products

| Method | Endpoint | Description |
|---|---|---|
| POST | `/Products/create` | Add a product |
| GET | `/Products/getall` | List all products |
| GET | `/Products/getby/{category}` | Filter by category |
| GET | `/Products/getbyname/{name}` | Search by name (partial, case-insensitive) |
| GET | `/Products/low-stock` | Products at or below their low-stock limit |
| GET | `/Products/getbyid/{id}` | Get one product by id |
| PUT | `/Products/update/{id}` | Update a product |
| PATCH | `/Products/restock/{id}` | Add stock to a product |
| DELETE | `/Products/delete/{id}` | Delete a product |

### Sales

| Method | Endpoint | Description |
|---|---|---|
| POST | `/Sales/create` | Create a bill and reduce stock |
| GET | `/Sales/getall` | List all sales, newest first |
| GET | `/Sales/getbyid/{id}` | Get one sale |
| GET | `/Sales/getbyname/{name}` | Search sales by customer name |
| DELETE | `/Sales/delete/{id}` | Cancel a sale and restore stock |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/Dashboard/summary` | Shop summary numbers |

## Request Examples

**Create a category** (`POST /Categories/create`)
```json
{ "category_name": "Dairy", "category_description": "Milk and cheese" }
```

**Create a product** (`POST /Products/create`)
```json
{
  "product_name": "Milk Pack 1L",
  "product_category": "Dairy",
  "product_price": 280,
  "product_stock": 50,
  "product_low_stock_limit": 10,
  "product_description": "Fresh milk"
}
```

**Restock** (`PATCH /Products/restock/{id}`)
```json
{ "restock_quantity": 20 }
```

**Create a sale** (`POST /Sales/create`). Only ids and quantities are sent; the server reads names and prices from the database.
```json
{
  "customer_name": "Ali",
  "items": [
    { "product_id": "665f1c2e9b1e8a3d4c5b6a7f", "quantity": 2 }
  ]
}
```

## Response Format

Success:
```json
{ "status": "success", "data": {}, "message": "..." }
```

Error:
```json
{ "status": "error", "data": [], "message": "..." }
```

Invalid request bodies (for example a negative price) are rejected by Pydantic with a `422` response.

## Business Rules

- Product and category names are unique, ignoring upper/lower case and extra spaces.
- A sale is validated completely before any stock changes. One bad item cancels the whole bill, and nothing is reduced.
- Stock is changed with MongoDB's `$inc`, not by reading and rewriting the value.
- A product has low stock when `stock <= low_stock_limit` (default 5).
- Today's sales on the dashboard are counted by calendar date.

## Possible Improvements

- Return proper HTTP status codes with `HTTPException` (201, 400, 404) instead of an error dictionary with status 200.
- Owner login with JWT.
- Pagination on the product list.
- Profit report using a `cost_price` field.
- Deploy the API (Render or Railway) and point the frontend to it.

## Credits

Project brief by Scorvix Solutions. The frontend was generated with AI and connected to this API.
