from decouple import config
import cloudinary
import cloudinary.uploader
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

SECRET_KEY = config('SECRET_KEY')

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
)

DATABASES = {
    "DB_NAME": config("POSTGRES_DB"),
    "USER": config("POSTGRES_USER"),
    "PASSWORD": config("POSTGRES_PASSWORD"),
    "HOST": config("PG_HOST"),
    "PORT": config("PG_PORT"),
}
