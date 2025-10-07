# apps/integrations/dpm/serializers.py
from rest_framework import serializers
from .models import Person, Relative, BorderCrossing
from apps.shared.utils import parse_date  # Sanani to'g'ri formatga o'tkazish uchun yordamchi funksiya


# --- Kiruvchi so'rov uchun ---
class PersonSearchRequestSerializer(serializers.Serializer):
    pinpp = serializers.CharField(max_length=14, required=True)
    doc_seria = serializers.CharField(max_length=10, required=False, allow_blank=True, default="")
    doc_number = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")


# --- DPM API javoblarini qabul qilish uchun (Deserialization) ---

class DPMBasePersonSerializer(serializers.Serializer):
    """DPM javobidagi shaxs va qarindosh uchun umumiy maydonlar"""
    person_id = serializers.IntegerField()
    pinpp = serializers.CharField(allow_null=True)
    doc_type_name = serializers.CharField(allow_null=True)
    doc_seria = serializers.CharField(allow_null=True)
    doc_number = serializers.CharField(allow_null=True)
    doc_start_date = serializers.CharField(allow_null=True)
    doc_end_date = serializers.CharField(allow_null=True)
    doc_give_place = serializers.CharField(allow_null=True)
    surname_latin = serializers.CharField(allow_null=True)
    name_latin = serializers.CharField(allow_null=True)
    patronym_latin = serializers.CharField(allow_null=True)
    surname_ru = serializers.CharField(allow_null=True)
    name_ru = serializers.CharField(allow_null=True)
    patronym_ru = serializers.CharField(allow_null=True)
    birth_date = serializers.CharField(allow_null=True)
    birth_place = serializers.CharField(allow_null=True)
    photo_id = serializers.IntegerField(allow_null=True)
    citizenship_name = serializers.CharField(allow_null=True)
    nationality_name = serializers.CharField(allow_null=True)
    sex_id = serializers.IntegerField(allow_null=True)
    is_doc_active = serializers.IntegerField(allow_null=True)
    status = serializers.CharField(allow_null=True)
    living_country = serializers.CharField(allow_null=True)
    living_region = serializers.CharField(allow_null=True)
    living_district = serializers.CharField(allow_null=True)
    living_place = serializers.CharField(allow_null=True)
    living_address_full = serializers.CharField(source='living_adress_full',
                                                allow_null=True)  # DPM javobidagi xatolikni to'g'rilaymiz


class DPMRelativeDeserializer(DPMBasePersonSerializer):
    """Qarindosh ma'lumotlarini qabul qilish uchun"""
    relation_type_name = serializers.CharField()


class DPMBorderCrossingDeserializer(serializers.Serializer):
    """Chegara kesish ma'lumotlarini qabul qilish uchun"""
    direction_type = serializers.CharField()
    reg_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    direction_country = serializers.CharField()
    trip_purpose_name = serializers.CharField()


# --- Chiqish javoblari uchun (DB dan olingan ma'lumotlarni Serialization) ---

class RelativeDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relative
        exclude = ('id', 'person', 'created_at')


class BorderCrossingDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorderCrossing
        exclude = ('id', 'person', 'created_at')


class PersonDBSerializer(serializers.ModelSerializer):
    """Bazada saqlangan shaxsning to'liq ma'lumotlari"""

    class Meta:
        model = Person
        fields = '__all__'


class PersonDetailsResponseSerializer(serializers.Serializer):
    """Barcha ma'lumotlarni birlashtirgan yakuniy javob serializeri"""
    person_data = PersonDBSerializer()
    photo_base64 = serializers.CharField(required=False, allow_null=True, help_text="Rasm base64 formatida")
    relatives = RelativeDBSerializer(many=True, required=False)
    border_crossings = BorderCrossingDBSerializer(many=True, required=False)

    class PersonDBSerializer(serializers.ModelSerializer):
        """Bazada saqlangan shaxsning to'liq ma'lumotlari"""
        photo_url = serializers.ImageField(source='photo', read_only=True)

        class Meta:
            model = Person
            fields = '__all__'
            extra_fields = ['photo_url']  # To be safe

    class PersonDetailsResponseSerializer(serializers.Serializer):
        """Barcha ma'lumotlarni birlashtirgan yakuniy javob serializeri"""
        person_data = PersonDBSerializer()
        # photo_base64 maydonini olib tashlaymiz, u endi person_data ichida URL sifatida keladi
        relatives = RelativeDBSerializer(many=True, required=False)
        border_crossings = BorderCrossingDBSerializer(many=True, required=False)
