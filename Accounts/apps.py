from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    AppConfig class for the Accounts app.

    Attributes:
        default_auto_field (str): Specifies the default auto field.
        name (str): The name of the app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "Accounts"

    def ready(self):
        pass
