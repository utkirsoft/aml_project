# apps/integrations/dpm/services.py
import httpx
import asyncio
from django.conf import settings
from typing import Dict, Any, Optional


class DPMGatewayService:
    """Tashqi DPM API'si bilan asinxron ishlash uchun servis"""

    def __init__(self):
        # .env yoki settings.py faylidan sozlamalarni oling
        self.base_url = getattr(settings, "DPM_BASE_URL", "http://10.130.12.77:7777/DWebServices/json/gcbpru")
        self.client = httpx.AsyncClient(timeout=50.0)
        self.default_params = {
            "req_name_unit": "Iqtisodiy jinoyatlarga qarshi kurashish departamenti",
            "req_doc_number": "ZRU-660-II",
            "is_consent": "Y"
        }

    async def _post_request(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint}"
        payload = {**data, **self.default_params}

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            # Loglash kerak (masalan, shared/logging_module yordamida)
            print(f"DPM API request error to {e.request.url}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            # Loglash kerak
            print(f"DPM API status error {e.response.status_code} for {e.request.url}: {e.response.text}")
            return None

    async def search_person(self, pinpp: str, doc_seria: str = "", doc_number: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "pinpp": pinpp,
            "doc_seria": doc_seria,
            "doc_number": doc_number,
            "surname": "", "name": "", "patronym": ""  # Java kodida bo'sh jo'natilgan
        }
        return await self._post_request("personSearch", payload)

    async def get_person_relatives(self, person_id: int) -> Optional[Dict[str, Any]]:
        return await self._post_request("personRel", {"person_id": str(person_id)})

    async def get_person_photo(self, photo_id: int) -> Optional[Dict[str, Any]]:
        return await self._post_request("personPhoto", {"photo_id": str(photo_id)})

    async def get_border_crossings(self, person_id: int) -> Optional[Dict[str, Any]]:
        return await self._post_request("personKg", {"person_id": str(person_id)})


# Singleton pattern
dpm_service = DPMGatewayService()
