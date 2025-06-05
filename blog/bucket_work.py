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


def make_image_name(email, ext):
    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    prefix = email.split('@')[0]
    return f"{prefix}_{timestamp}.{ext}"


def get_extension_from_base64(base64_str):
    start = base64_str.find("data:image/")
    if start == -1:
        raise ValueError("Base64 string does not contain 'data:image/'")
    start += len("data:image/")
    end = base64_str.find(";", start)
    if end == -1:
        raise ValueError(
            "Base64 string does not contain ';' after the image type")
    ext = base64_str[start:end].lower()
    return ext


def upload_image_to_bucket(email, image_base64):
    ext = get_extension_from_base64(image_base64)
    image_name = make_image_name(email, ext)

    if "," in image_base64:
        image_data = image_base64.split(",")[1]
    else:
        image_data = image_base64

    image = base64.b64decode(image_data)

    supabase.storage.from_(bucket_name).upload(  # type: ignore
        image_name,
        image,
        file_options={"content-type": f"image/{ext}"}
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


def replace_image_in_bucket(old_url, email, new_image_base64):
    delete_image_from_bucket(old_url)
    new_url = upload_image_to_bucket(email, new_image_base64)
    return new_url
