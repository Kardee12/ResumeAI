from Core.models import UserProfile


def generate_resume_text(user, data):
    profile = UserProfile.objects.get(user=user)
    text_parts = [
        f"Name: {user.first_name} {user.last_name}",
        f"Email: {user.email}",
        f"Location: {profile.location}",
        f"Professional Summary:\n{profile.bio}",
        "\nWork Experience:"
    ]
    for i in range(1, 4):
        text_parts.append(
            f"\nJob Title {i}: {data.get(f'job_title_{i}')}\n"
            f"Company Name {i}: {data.get(f'company_name_{i}')}\n"
            f"Start Date {i}: {data.get(f'start_date_{i}')}\n"
            f"End Date {i}: {data.get(f'end_date_{i}')}\n"
            f"Job Description {i}:\n{data.get(f'job_description_{i}')}"
        )
    text_parts.append("\nEducation:")
    text_parts.append(
        f"Degree: {data.get('degree')}\n"
        f"Institution Name: {data.get('institution_name')}\n"
        f"Education Start Date: {data.get('education_start_date')}\n"
        f"Education End Date: {data.get('education_end_date')}"
    )
    text_parts.append("\nSkills:")
    for i in range(1, 11):
        skill = data.get(f'skill_{i}')
        if skill:
            text_parts.append(f"Skill {i}: {skill}")

    return "\n".join(text_parts)
