from decouple import config
import cloudinary
import cloudinary.uploader

SECRET_KEY = config('SECRET_KEY')

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
)