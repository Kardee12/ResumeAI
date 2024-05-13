import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ResumeAI.settings')
django.setup()
from django.apps import apps
from django.db import transaction, IntegrityError


def clear_data():
    """
    Clear all data from the database tables.

    This function iterates over all models registered in the Django app and deletes all records from their
    corresponding database tables. It uses a transaction to ensure atomicity, and it prints a message for each
    model table cleared. If any integrity error occurs during the deletion process, it catches the exception
    and prints an error message.

    Note: This function should be used with caution as it will permanently delete all data from the database.

    """
    with transaction.atomic():
        try:
            for model in apps.get_models():
                model.objects.all().delete()
                print(f"Cleared data from {model._meta.db_table}")
        except IntegrityError as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    confirm = input("Are you sure you want to delete all data from the database? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_data()
    else:
        print("Operation cancelled.")
