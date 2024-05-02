from django.db import transaction

from Core.models import Skill, UserProfile


def update_user_skills(user, skill_names):
    with transaction.atomic():
        skills = []
        for name in skill_names:
            skill, created = Skill.objects.get_or_create(name=name)
            skills.append(skill)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.skills.set(skills)
        profile.save()

    return profile
