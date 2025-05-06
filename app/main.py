import logging.config
import os
from fastapi import FastAPI
from app.db.database import engine
from app.models import ticket, message, user
from app.routes import tickets, users

LOGGING_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(LOGGING_CONFIG_PATH, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Create database tables
ticket.Base.metadata.create_all(bind=engine)
message.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple Ticketing System",
    description="A RESTful ticketing system with tree-structured message support.",
    version="0.1.0",
    docs_url="/docs",
    openapi_tags=[
        {"name": "Tickets", "description": "Operations related to tickets and messages"},
        {"name": "Users", "description": "Operations related to users"}
    ]
)

app.include_router(tickets.router)
app.include_router(users.router)

@app.get("/")
async def root():
    """Root endpoint. Returns a Hello World message."""
    logger.info("Root endpoint was called")
    return {"message": "Hello World"}