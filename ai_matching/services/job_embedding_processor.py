from jobs.models import Job
from jobs.models import JobEmbedding

from .gemini_embeddings import generate_embedding


def process_job_embeddings(job_id):

    try:
        job = Job.objects.get(
            job_id=job_id
        )

        skills_text = " ".join(
            job.required_skills
        )

        experience_text = " ".join(
            job.required_experience
        )

        education_text = " ".join(
            job.required_education
        )

        skills_embedding = generate_embedding(
            skills_text
        )

        experience_embedding = generate_embedding(
            experience_text
        )

        education_embedding = generate_embedding(
            education_text
        )
       

        JobEmbedding.objects.update_or_create(
            job=job,
            defaults={
                "skills_embedding": skills_embedding,
                "experience_embedding": experience_embedding,
                "education_embedding": education_embedding,
            }
        )

    except Exception as e:
        print(f"Embedding Error: {e}")