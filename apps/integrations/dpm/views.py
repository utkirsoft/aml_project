# apps/integrations/dpm/views.py
import asyncio
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    PersonSearchRequestSerializer, PersonDetailsResponseSerializer,
    DPMBasePersonSerializer, DPMRelativeDeserializer, DPMBorderCrossingDeserializer
)
from .services import dpm_service
from .models import Person, Relative, BorderCrossing
from apps.shared.utils import parse_date, save_photo_from_base64


class PersonDetailsAPIView(APIView):
    """
    Asinxron view: shaxsni qidiradi, ma'lumotlarini to'liq keshlaydi
    va barcha bog'liq ma'lumotlarni (qarindoshlar, rasm, chegara) qaytaradi.
    """

    async def post(self, request, *args, **kwargs):
        request_serializer = PersonSearchRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        valid_data = request_serializer.validated_data
        pinpp = valid_data['pinpp']

        # O'zimizning bazadan shaxsni va unga bog'liq ma'lumotlarni olish
        person = await Person.objects.filter(pinpp=pinpp).prefetch_related(
            'relatives', 'border_crossings'
        ).afirst()

        photo_id = None
        if not person:
            # Agar bazada yo'q bo'lsa, DPM'dan qidirish
            dpm_person_data = await dpm_service.search_person(**valid_data)
            if not dpm_person_data or not isinstance(dpm_person_data, list) or not dpm_person_data[0].get('PERSON_ID'):
                return Response({"detail": "Shaxs DPM tizimida topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            # DPM javobini validatsiya qilish
            dpm_serializer = DPMBasePersonSerializer(data=dpm_person_data[0])
            if not dpm_serializer.is_valid():
                return Response(dpm_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            clean_data = dpm_serializer.validated_data
            photo_id = clean_data.get('photo_id')

            # Atomar tranzaksiya ichida barcha ma'lumotlarni saqlash
            async with transaction.atomic():
                person = await Person.objects.acreate(
                    doc_start_date=parse_date(clean_data.get('doc_start_date')),
                    doc_end_date=parse_date(clean_data.get('doc_end_date')),
                    birth_date=parse_date(clean_data.get('birth_date')),
                    **clean_data
                )
        else:
            photo_id = person.photo_id

        # Parallel ravishda qo'shimcha ma'lumotlarni so'rash
        tasks = [
            dpm_service.get_person_relatives(person.person_id),
            dpm_service.get_border_crossings(person.person_id),
        ]
        if photo_id:
            tasks.append(dpm_service.get_person_photo(photo_id))

        results = await asyncio.gather(*tasks)
        relatives_res, crossings_res = results[0], results[1]
        photo_res = results[2] if photo_id else None
        # Rasmni fayl sifatida saqlash
        if photo_res and photo_res.get('photo'):
            await save_photo_from_base64(person, photo_res.get('photo'))

        # Olingan ma'lumotlarni bazaga saqlash
        if relatives_res:
            relatives_deserializer = DPMRelativeDeserializer(data=relatives_res, many=True)
            if relatives_deserializer.is_valid():
                await Relative.objects.filter(person=person).adelete()  # Eskilarini o'chirish
                relative_objects = [Relative(person=person, **rel_data) for rel_data in
                                    relatives_deserializer.validated_data]
                await Relative.objects.abulk_create(relative_objects)

        if crossings_res:
            crossings_deserializer = DPMBorderCrossingDeserializer(data=crossings_res, many=True)
            if crossings_deserializer.is_valid():
                await BorderCrossing.objects.filter(person=person).adelete()  # Eskilarini o'chirish
                crossing_objects = [BorderCrossing(person=person, **cross_data) for cross_data in
                                    crossings_deserializer.validated_data]
                await BorderCrossing.objects.abulk_create(crossing_objects)

        # Bazadan yangilangan ma'lumotlarni qayta olish
        person = await Person.objects.prefetch_related('relatives', 'border_crossings').aget(pk=person.pk)

        # Yakuniy javobni tayyorlash
        response_data = {
            "person_data": person,
            "relatives": person.relatives.all(),
            "border_crossings": person.border_crossings.all(),
            "photo_base64": photo_res.get('photo') if photo_res else None
        }

        final_serializer = PersonDetailsResponseSerializer(response_data)
        return Response(final_serializer.data, status=status.HTTP_200_OK)
