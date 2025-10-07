# apps/integrations/dpm/models.py
from django.db import models
from django.utils import timezone


class Person(models.Model):
    """DPM'dan olingan shaxsning asosiy va batafsil ma'lumotlari"""
    # Asosiy identifkatorlar
    person_id = models.BigIntegerField(unique=True, db_index=True, help_text="DPM tizimidagi unikal ID")
    photo_id = models.BigIntegerField(null=True, blank=True, help_text="DPM tizimidagi rasm IDsi")
    pinpp = models.CharField(max_length=14, unique=True, db_index=True, help_text="JSHSHIR")

    # F.I.O. (Lotin va Kirill)
    surname_latin = models.CharField(max_length=100)
    name_latin = models.CharField(max_length=100)
    patronym_latin = models.CharField(max_length=100, null=True, blank=True)
    surname_ru = models.CharField(max_length=100, null=True, blank=True)
    name_ru = models.CharField(max_length=100, null=True, blank=True)
    patronym_ru = models.CharField(max_length=100, null=True, blank=True)

    # Hujjat ma'lumotlari
    doc_type_name = models.CharField(max_length=255, null=True, blank=True)
    doc_seria = models.CharField(max_length=10, null=True, blank=True)
    doc_number = models.CharField(max_length=20, null=True, blank=True)
    doc_start_date = models.DateField(null=True, blank=True)
    doc_end_date = models.DateField(null=True, blank=True)
    doc_give_place = models.CharField(max_length=255, null=True, blank=True)
    is_doc_active = models.IntegerField(null=True, blank=True)

    # Shaxsiy ma'lumotlar
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=255, null=True, blank=True)
    sex_id = models.IntegerField(null=True, blank=True, help_text="1-Erkak, 2-Ayol")
    nationality_name = models.CharField(max_length=100, null=True, blank=True)
    citizenship_name = models.CharField(max_length=100, null=True, blank=True)

    # Yashash manzili
    living_country = models.CharField(max_length=100, null=True, blank=True)
    living_region = models.CharField(max_length=100, null=True, blank=True)
    living_district = models.CharField(max_length=100, null=True, blank=True)
    living_place = models.CharField(max_length=255, null=True, blank=True)
    living_address_full = models.CharField(max_length=500, null=True, blank=True)

    # Rasm faylini saqlash uchun yangi maydon
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, help_text="Shaxsning rasmi")

    # Meta ma'lumotlar
    status = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.surname_latin} {self.name_latin} ({self.pinpp})"


class Relative(models.Model):
    """Shaxsning qarindoshlari"""
    person = models.ForeignKey(Person, related_name='relatives', on_delete=models.CASCADE)
    relation_type_name = models.CharField(max_length=100, help_text="Qarindoshlik turi (ota, ona, farzand)")

    # Qarindoshning ma'lumotlari (Person modeli bilan deyarli bir xil)
    relative_person_id = models.BigIntegerField()
    pinpp = models.CharField(max_length=14, db_index=True)
    surname_latin = models.CharField(max_length=100)
    name_latin = models.CharField(max_length=100)
    patronym_latin = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} -> {self.relation_type_name}: {self.surname_latin} {self.name_latin}"


class BorderCrossing(models.Model):
    """Shaxsning chegara kesib o'tish ma'lumotlari"""
    person = models.ForeignKey(Person, related_name='border_crossings', on_delete=models.CASCADE)

    direction_type = models.CharField(max_length=50, help_text="P-kirish; M-chiqish")
    reg_date = models.DateTimeField(help_text="Chegara kesish sanasi va vaqti")
    direction_country = models.CharField(max_length=100)
    trip_purpose_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} crossed border on {self.reg_date}"

    # apps/integrations/dpm/models.py

    # ... avvalgi Person, Relative, BorderCrossing modellari ...

    class DPMQuery(models.Model):
        """Excel fayllaridan o'qilgan ommaviy so'rovlarni saqlash uchun model"""
        QUERY_TYPE_CHOICES = [
            (1, 'F.I.O. orqali'),
            (2, 'Pasport seriya va raqami orqali'),
            (3, 'JSHSHIR (PINFL) orqali'),
        ]

        # So'rov ma'lumotlari
        first_name = models.CharField(max_length=100, null=True, blank=True)
        last_name = models.CharField(max_length=100, null=True, blank=True)
        patronym = models.CharField(max_length=100, null=True, blank=True)
        passport_serial = models.CharField(max_length=10, null=True, blank=True)
        passport_number = models.CharField(max_length=20, null=True, blank=True)
        pinfl = models.CharField(max_length=14, null=True, blank=True, db_index=True)

        query_type = models.IntegerField(choices=QUERY_TYPE_CHOICES)

        # Status
        STATUS_CHOICES = [
            ('new', 'Yangi'),
            ('processing', 'Jarayonda'),
            ('completed', 'Bajarildi'),
            ('error', 'Xatolik'),
        ]
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

        # Meta
        created_at = models.DateTimeField(auto_now_add=True)
        processed_at = models.DateTimeField(null=True, blank=True)

        def __str__(self):
            if self.query_type == 1:
                return f"{self.last_name} {self.first_name}"
            elif self.query_type == 2:
                return f"{self.passport_serial}{self.passport_number}"
            return self.pinfl

        class Meta:
            db_table = 'dpm_queries'  # Jadval nomini aniq belgilaymiz
            verbose_name = "Ommaviy so'rov (DPM)"
            verbose_name_plural = "Ommaviy so'rovlar (DPM)"
            ordering = ['-created_at']
