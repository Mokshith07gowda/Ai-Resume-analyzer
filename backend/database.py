from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import certifi
from config import settings
from logger import get_logger

logger = get_logger(__name__)

client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
    global client, database
    try:
        client = AsyncIOMotorClient(
            settings.mongodb_url,
            server_api=ServerApi("1"),
            maxPoolSize=10,
            minPoolSize=1,
            tls=True,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=False,  # secure in prod
        )
        await client.admin.command("ping")
        database = client[settings.database_name]
        logger.info(f"Connected to MongoDB | DB: {settings.database_name}")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise


async def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")


def get_database():
    return database

def get_users_collection():
    return database.users

def get_resumes_collection():
    return database.resumes

def get_job_descriptions_collection():
    return database.job_descriptions

def get_analysis_results_collection():
    return database.analysis_results