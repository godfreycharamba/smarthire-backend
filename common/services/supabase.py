import os
import uuid
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_file(file, folder):
    file_ext = file.name.split(".")[-1]
    file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_("media").upload(
        file_name,
        file.read(),
        {"content-type": file.content_type}
    )

    return supabase.storage.from_("media").get_public_url(file_name)