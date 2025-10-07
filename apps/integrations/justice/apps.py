from django.apps import AppConfig


class JusticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.integrations.justice'
    verbose_name = "Notarius integratsiyasi"  # Keyingi punkt uchun

    def ready(self):
        print("Notarius integratsiyasi moduli ishga tushdi!")
        # Bu yerga signallarni ulash yoki boshqa boshlang'ich kod yoziladi
