import cloudinary
from cloudinary.uploader import upload
from  cloudinary.utils import  cloudinary_url
import os

from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

bruh = cloudinary.uploader.upload('/home/lonewolf/Pictures/Screenshot from 2021-03-25 22-13-41.png',public_id='petbook/rajesh/1')
#bruh = cloudinary.utils.cloudinary_url('petbook/rajesh/1')
#cloudinary.uploader.destroy()

print(bruh)
print(type(bruh))