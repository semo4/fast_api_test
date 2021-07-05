from controller import address, users
from fastapi import FastAPI

app = FastAPI(version=1.0, description='User Address Api')
app.include_router(users.router)
app.include_router(address.router)
