# apps/shared/utils.py
import base64
from datetime import datetime
from django.core.files.base import ContentFile
from apps.integrations.dpm.models import Person  # To'liq import yo'li


def parse_date(date_string: str | None):
    """'DD.MM.YYYY' formatidagi satrni date obyektiga o'tkazadi."""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, '%d.%m.%Y').date()
    except (ValueError, TypeError):
        return None


async def save_photo_from_base64(person: Person, base64_string: str | None):
    """
    Base64 formatdagi satrni rasmga o'giradi va Person modelining
    'photo' maydoniga saqlaydi.
    Fayl nomi: <pinfl>_<dd.mm.yyyy>.jpg
    """
    if not base64_string or not person.pinpp:
        return

    try:
        image_data = base64.b64decode(base64_string)
        current_date = datetime.now().strftime('%d.%m.%Y')
        filename = f"{person.pinpp}_{current_date}.jpg"
        photo_file = ContentFile(image_data, name=filename)

        person.photo = photo_file
        await person.asave(update_fields=['photo'])

    except (ValueError, TypeError) as e:
        print(f"PINFL {person.pinpp} uchun rasmni saqlashda xatolik: {e}")