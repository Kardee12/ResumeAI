import os
import django
import ResumeAI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ResumeAI.settings')
django.setup()


def clear_data():
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
