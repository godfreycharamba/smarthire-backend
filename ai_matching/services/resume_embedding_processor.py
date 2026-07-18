from profiles.models import (
    JobSeekerProfile,
    ResumeEmbedding
)

from .gemini_embeddings import generate_embedding
from .helper_functions import profile_data_to_text


def process_resume_embeddings(profile_id):

    try:

        profile = JobSeekerProfile.objects.get(profile_id=profile_id)

        skills_text = profile_data_to_text(profile.skills)

        experience_text = profile_data_to_text(profile.experience)

        education_text = profile_data_to_text(profile.education)

        skills_embedding = generate_embedding(
            skills_text
        )

        experience_embedding = generate_embedding(
            experience_text
        )

        education_embedding = generate_embedding(
            education_text
        )

        ResumeEmbedding.objects.update_or_create(
            profile=profile,
            defaults={
                "skills_embedding": skills_embedding,
                "experience_embedding": experience_embedding,
                "education_embedding": education_embedding,
            }
        )

    except Exception as e:
        print(f"Resume Embedding Error: {e}")