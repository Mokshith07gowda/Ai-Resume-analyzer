"""
MongoDB Database Configuration and Connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os

MONGODB_URL = "mongodb+srv://asterinfinity8_db_user:HVAUST9BplT1PIsr@cluster0.rh7lk3w.mongodb.net/"
DATABASE_NAME = "ai_resume_analyzer"

client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
    """
    Connect to MongoDB database
    """
    global client, database
    try:
        client = AsyncIOMotorClient(
            MONGODB_URL,
            server_api=ServerApi('1'),
            maxPoolSize=10,
            minPoolSize=1
        )
        
        await client.admin.command('ping')
        
        database = client[DATABASE_NAME]
        
        print(f"✓ Connected to MongoDB successfully!")
        print(f"✓ Database: {DATABASE_NAME}")
        
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        raise e


async def close_mongo_connection():
    """
    Close MongoDB connection
    """
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")


def get_database():
    """
    Get database instance
    """
    return database


def get_users_collection():
    """Get users collection"""
    return database.users


def get_resumes_collection():
    """Get resumes collection"""
    return database.resumes


def get_job_descriptions_collection():
    """Get job descriptions collection"""
    return database.job_descriptions


def get_analysis_results_collection():
    """Get analysis results collection"""
    return database.analysis_results
