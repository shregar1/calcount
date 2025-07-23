import os
import bcrypt
import sys

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configurations.db import DBConfiguration, DBConfigurationDTO

from models import Base
from repositories.user import UserRepository

logger.remove(0)
logger.add(
    sys.stderr,
    colorize=True,
    format=(
        "<green>{time:MMMM-D-YYYY}</green> | <black>{time:HH:mm:ss}</black> | "
        "<level>{level}</level> | <cyan>{message}</cyan> | "
        "<magenta>{name}:{function}:{line}</magenta> | "
        "<yellow>{extra}</yellow>"
    ),
)

# Load environment variables from .env file
load_dotenv()

logger.info("Loading Configurations")
db_configuration: DBConfigurationDTO = DBConfiguration().get_config()
logger.info("Loaded Configurations")

# Access environment variables
logger.info("Loading environment variables")
APP_NAME: str = os.environ.get("APP_NAME")
SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
)
BASE_URL: str = os.getenv("BASE_URL")
logger.info("Loaded environment variables")

logger.info("Initializing PostgreSQL database")
engine = create_engine(
    db_configuration.connection_string.format(
        user_name=db_configuration.user_name,
        password=db_configuration.password,
        host=db_configuration.host,
        port=db_configuration.port,
        database=db_configuration.database,
    )
)
Session = sessionmaker(bind=engine)
db_session = Session()
Base.metadata.create_all(engine)
logger.info("Initialized PostgreSQL database")

admin_user = UserRepository(
    urn=None, session=db_session
).retrieve_record_by_email_and_password(
    email=os.getenv("ADMIN_EMAIL"),
    password=bcrypt.hashpw(
        os.getenv("ADMIN_PASSWORD").encode("utf8"),
        os.getenv("BCRYPT_SALT").encode("utf8"),
    ).decode("utf8"),
)

if admin_user is None:
    raise RuntimeError("Admin user not found")

unprotected_routes: set = {
    "/health",
    "/login",
    "/register",
}

db_session.commit()
