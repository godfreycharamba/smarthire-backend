from ai_matching.services.resume_extractor import extract_resume_text
from ai_matching.services.gemini_resume_parser import parse_resume
from common.services.supabase import upload_file
from ai_matching.services.resume_embedding_processor import process_resume_embeddings
import traceback
import os
from django.core.files.uploadedfile import SimpleUploadedFile



from profiles.models import JobSeekerProfile
import mimetypes


def get_content_type(file_path):

    content_type, _ = mimetypes.guess_type(
        file_path
    )

    return content_type or "application/octet-stream"



def process_resume(profile_id, file_path):

    profile = JobSeekerProfile.objects.get(
        profile_id=profile_id
    )

    try:

        profile.processing_status = "processing"
        profile.save()


        with open(file_path, "rb") as resume:


            # Extract resume text
            resume_text = extract_resume_text(
                resume
            )


            # Gemini parsing
            parsed_data = parse_resume(
                resume_text
            )


            # Upload
            resume.seek(0)

            uploaded_file = SimpleUploadedFile(
                name=os.path.basename(file_path),
                content=resume.read(),
                content_type=get_content_type(file_path)
            )


            resume_url = upload_file(
                file=uploaded_file,
                folder="resumes"
            )


        profile.resume_url = resume_url

        profile.skills = parsed_data.get(
            "skills",
            []
        )

        profile.education = parsed_data.get(
            "education",
            []
        )

        profile.experience = parsed_data.get(
            "experience",
            []
        )


        profile.processing_status = "completed"

        profile.save()


        process_resume_embeddings(
            profile.profile_id
        )


    except Exception:

        

        profile.processing_status = "failed"
        profile.save()

        traceback.print_exc()


    finally:

        # remove temporary file
        if os.path.exists(file_path):
            os.remove(file_path)