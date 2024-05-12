from django.db import transaction

from Core.models import UserSkill, UserProfile


def create_user_skills(user, skill_names):
    with transaction.atomic():
        skills = []
        for name in skill_names:
            skill, created = UserSkill.objects.get_or_create(name=name)
            skills.append(skill)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.skills.set(skills)
        profile.save()

    return profile


def update_user_skills(user, skill_names):
    with transaction.atomic():
        profile = UserProfile.objects.get(user=user)
        for skill_name in skill_names:
            skill, created = UserSkill.objects.get_or_create(name=skill_name)
            profile.skills.add(skill)
        profile.save()
