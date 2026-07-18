from sklearn.metrics.pairwise import cosine_similarity

from jobs.models import JobEmbedding
from profiles.models import ResumeEmbedding


def calculate_similarity(vector1, vector2):
    print(vector1)
    print(vector2)

    if not vector1 or not vector2:
        return 0.00

    score = cosine_similarity(
        [vector1],
        [vector2]
    )[0][0]

    return round(score * 100, 2)


def calculate_application_scores(job, applicant):

    try:

        job_embedding = JobEmbedding.objects.get(
            job=job
        )

        applicant_embedding = ResumeEmbedding.objects.get(
            profile=applicant
        )

    except (
        JobEmbedding.DoesNotExist,
        ResumeEmbedding.DoesNotExist
    ):
        print("Job and resume embeddings does not exist")
        return {
            
            "skills_score": 0.00,
            "experience_score": 0.00,
            "education_score": 0.00,
            "total_match_score": 0.00,
        }

    skills_score = calculate_similarity(
        applicant_embedding.skills_embedding,
        job_embedding.skills_embedding
    )

    experience_score = calculate_similarity(
        applicant_embedding.experience_embedding,
        job_embedding.experience_embedding
    )

    education_score = calculate_similarity(
        applicant_embedding.education_embedding,
        job_embedding.education_embedding
    )

    total_match_score = round(
        (
            skills_score * 0.5 +
            experience_score * 0.3 +
            education_score * 0.2
        ),
        2
    )
    print("Cosine calculations done: ")
    print(education_score)
    print(experience_score)
    print(skills_score)

    return {
        "skills_score": skills_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "total_match_score": total_match_score,
    }