from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from routes.categories_routes import categoryRoutes
from routes.dashboard_routes import dashboardRoutes
from routes.products_routes import productsRoutes
from routes.sales_routes import salesRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoryRoutes,prefix="/Categories",tags=["Categories"])
app.include_router(productsRoutes,prefix="/Products",tags=["Products"])
app.include_router(salesRoutes,prefix="/Sales",tags=["Sales"])
app.include_router(dashboardRoutes,prefix="/Dashboard",tags=["Dashboard"])

@app.get("/")
def test():
    return ("server is up and running")
