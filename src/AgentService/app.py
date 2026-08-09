from AgentService.routers.exception_handler import register_handler
from AgentService.routers.auth import auth_router
from fastapi import FastAPI


app = FastAPI()

register_handler(app)

app.include_router(auth_router, prefix="/v1")