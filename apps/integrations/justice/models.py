from django.db import models
from apps.shared.logging_module.models import ApiActionLog


# Eslatma: Bu modellar `ApiActionLog` bilan bog'lanadi. Har bir saqlangan
# ma'lumotlar to'plami qaysi API so'roviga tegishli ekanligini bilish uchun.

class RegistryData(models.Model):
    """
    Notarial harakat haqidagi asosiy ma'lumot.
    Java'dagi `RegistryData` sinfiga mos keladi.
    """
    log = models.ForeignKey(
        ApiActionLog,
        on_delete=models.CASCADE,
        related_name='notary_registry_data',
        verbose_name="API Log Zapisi"
    )
    regdate = models.DateField(
        "Дата реестра",
        help_text="Notarial harakatning ro'yxatga olingan sanasi",
        null=True, blank=True
    )
    regnum = models.CharField(
        "Номер реестра",
        max_length=50,
        help_text="Notarial harakatning reyestr raqami",
        null=True, blank=True
    )
    office = models.CharField(
        "Наименование нот.конторы",
        max_length=255,
        help_text="Notarial idora nomi",
        null=True, blank=True
    )
    notary_code = models.CharField(
        "Код нотариуса",
        max_length=10,
        help_text="Notariusning litsenziya kodi",
        null=True, blank=True
    )
    notary_fio = models.CharField(
        "ФИО нотариуса",
        max_length=255,
        help_text="Notariusning F.I.Sh.",
        null=True, blank=True
    )
    type = models.CharField(
        "Тип нот.действия",
        max_length=255,
        help_text="Notarial harakat turi",
        null=True, blank=True
    )
    state = models.CharField(
        "Состояние нот.действия",
        max_length=100,
        help_text="Notarial harakat holati (masalan, 'Ro'yxatga olingan')",
        null=True, blank=True
    )
    relative = models.IntegerField(
        "Родственные связи",
        help_text="Qarindoshlik aloqalari (1-boshqa shaxslar, 2-qarindoshlar)",
        null=True, blank=True
    )
    term_from = models.DateField(
        "Дата начала аренды",
        help_text="Ijara boshlanish sanasi",
        null=True, blank=True
    )
    term_to = models.DateField(
        "Дата конца аренды",
        help_text="Ijara tugash sanasi",
        null=True, blank=True
    )
    sum = models.DecimalField(
        "Сумма за один месяц аренды",
        max_digits=20, decimal_places=2,
        help_text="Bir oylik ijara summasi",
        null=True, blank=True
    )
    total_sum = models.DecimalField(
        "Общая сумма аренды",
        max_digits=20, decimal_places=2,
        help_text="Ijarani umumiy summasi",
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.regnum} - {self.notary_fio if self.notary_fio else 'Noma`lum'}"

    class Meta:
        verbose_name = "Данные реестра"
        verbose_name_plural = "Данные реестров"
        db_table = 'notary_registry_data'


class Member(models.Model):
    """
    Notarial harakat ishtirokchisi (sotuvchi, oluvchi va hokazo).
    Java'dagi `Member` sinfiga mos keladi.
    """
    registry_data = models.ForeignKey(
        RegistryData,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name="Запись реестра"
    )
    type = models.CharField(
        "Тип участника",
        max_length=100,
        help_text="Ishtirokchi turi (masalan, 'sotuvchi')",
        null=True, blank=True
    )
    surname = models.CharField("Фамилия", max_length=100, null=True, blank=True)
    name = models.CharField("Имя", max_length=255, help_text="Ismi yoki tashkilot nomi", null=True, blank=True)
    lastname = models.CharField("Отчество", max_length=100, null=True, blank=True)
    birthdate = models.DateField("Дата рождения", null=True, blank=True)
    inn = models.CharField("ИНН", max_length=9, null=True, blank=True)
    pin = models.CharField("ПИНФЛ", max_length=14, null=True, blank=True)
    pass_serial = models.CharField("Серия паспорта", max_length=10, null=True, blank=True)
    pass_num = models.CharField("Номер паспорта", max_length=20, null=True, blank=True)
    address = models.CharField("Адрес", max_length=500, null=True, blank=True)
    represent_to = models.CharField("Представляет интересы", max_length=255,
                                    help_text="Kimning nomidan ish ko'rayotgani", null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Участник действия"
        verbose_name_plural = "Участники действия"
        db_table = 'notary_member'


class Subject(models.Model):
    """
    Notarial harakat obyekti (avtomobil, ko'chmas mulk va hokazo).
    Java'dagi `Subject` sinfiga mos keladi.
    """
    registry_data = models.ForeignKey(
        RegistryData,
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name="Запись реестра"
    )
    type = models.CharField(
        "Тип объекта",
        max_length=100,
        help_text="Obyekt turi (masalan, 'Yengil avtomobil')",
        null=True, blank=True
    )
    cadastrenum = models.CharField("Кадастровый номер", max_length=50, null=True, blank=True)
    mark = models.CharField("Марка/модель", max_length=100, null=True, blank=True)
    regnum = models.CharField("Гос. номер", max_length=20, null=True, blank=True)
    yearcreate = models.PositiveIntegerField("Год выпуска", null=True, blank=True)
    color = models.CharField("Цвет", max_length=50, null=True, blank=True)
    techserial = models.CharField("Серия тех. паспорта", max_length=10, null=True, blank=True)
    technum = models.CharField("Номер тех. паспорта", max_length=20, null=True, blank=True)
    price = models.DecimalField("Стоимость", max_digits=20, decimal_places=2, null=True, blank=True)
    address = models.CharField("Адрес объекта", max_length=500, null=True, blank=True)
    quadrature = models.FloatField("Площадь (кв.м.)", null=True, blank=True)

    def __str__(self):
        return self.type or "Noma'lum obyekt"

    class Meta:
        verbose_name = "Объект действия"
        verbose_name_plural = "Объекты действия"
        db_table = 'notary_subject'
