def safe_divide(numerator, denominator):
    """Avoid division by zero."""
    if denominator == 0:
        return 0
    return numerator / denominator


def compute_score(resume_data: dict, job_requirements: dict, weights: dict) -> float:
    """
    Calculate weighted candidate score.

    Parameters
    ----------
    resume_data : dict
        Counts of matches found in resume.

    job_requirements : dict
        Total counts from job description.

    weights : dict
        Weight configuration.

    Returns
    -------
    float
        Final candidate score (0–1 range)
    """

    # Normalize component scores
    s_req = safe_divide(
        resume_data["required_skills_found"], job_requirements["required_skills_total"]
    )

    s_pref = safe_divide(
        resume_data["preferred_skills_found"],
        job_requirements["preferred_skills_total"],
    )

    e_exp = safe_divide(
        resume_data["experience_matches"],
        job_requirements["experience_indicators_total"],
    )

    k_key = safe_divide(
        resume_data["keyword_matches"], job_requirements["keywords_total"]
    )

    # Weighted sum
    final_score = (
        s_req * weights["required_skills"]
        + s_pref * weights["preferred_skills"]
        + e_exp * weights["experience"]
        + k_key * weights["keywords"]
    )

    return round(final_score, 4)
