from dotenv import load_dotenv
import os
from supabase import create_client, Client
import base64
import datetime


load_dotenv()


supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
bucket_name = os.environ['BUCKET_NAME']

if not supabase_url or not supabase_key or not bucket_name:
    raise RuntimeError(
        "One or more required environment variables are missing: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, BUCKET_NAME")


supabase: Client = create_client(supabase_url, supabase_key)


def make_image_name(email):
    return email[0:email.index('@')] + str(datetime.datetime)


def upload_image_to_bucket(email, image_base64):

    image = base64.b64decode(image_base64)
    image_name = make_image_name(email)
    data = supabase.storage.from_(bucket_name).upload(  # type: ignore
        image_name,
        image,
        file_options={"content-type": "image/*"}
    )
    url = supabase.storage.from_(bucket_name).get_public_url(image_name)
    return url


def get_file_path(url, bucket_name):
    try:
        index = url.index(bucket_name)
        return url[index + len(bucket_name) + 1:-1]
    except ValueError:
        return url


def delete_image_from_bucket(url):
    file_path = get_file_path(url, bucket_name)
    result = supabase.storage.from_(bucket_name).remove([file_path])
    return result
