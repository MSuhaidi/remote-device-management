import os

API_TOKEN = os.getenv("API_TOKEN")
APP_NAME = os.getenv("APP_NAME","RemoteDeviceDashboard")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
