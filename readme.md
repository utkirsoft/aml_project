```aml_project/
├── .venv/                  # Virtual muhit papkasi
├── aml/                    # Django loyihasining asosiy sozlamalari
│   ├── __init__.py
│   ├── settings.py         # Asosiy sozlamalar fayli
│   ├── urls.py             # Asosiy URL manzillar
│   └── ...
│
├── apps/                   # BARCHA ilovalar uchun asosiy papka
│   ├── __init__.py
│   │
│   ├── core/               # Asosiy biznes logikasi va umumiy modellar
│   ├── users/              # Foydalanuvchilarni boshqarish (auth, profillar)
│   ├── rbac/               # Rolga asoslangan ruxsatlar (django-guardian)
│   ├── documents/            # Hujjatlar bilan ishlash (import/export, generatsiya)
│   ├── ai/                   # Sun'iy intellekt va NLP modullari
│   │
│   ├── integrations/         # Barcha tashqi API integratsiyalari uchun PAKET
│   │   ├── __init__.py
│   │   ├── notary/           # Notarius uchun alohida ilova
│   │   ├── tax/              # Soliq uchun alohida ilova
│   │   └── bank_accounts/    # Bank hisoblari uchun alohida ilova
│   │
│   └── shared/               # Barcha ilovalar uchun umumiy modullar
│       ├── __init__.py
│       └── logging_module/   # Markazlashtirilgan loglash ilovasi
│
├── common/                 # Loyiha uchun umumiy, ilovaga bog'liq bo'lmagan yordamchilar (utils)
│   ├── __init__.py
│   ├── encryption.py       # Shifrlash funksiyalari
│   ├── file_helpers.py     # Fayllar bilan ishlash yordamchilari
│   └── ...
│
├── configs/                # Konfiguratsiya fayllari
│   └── api_config.json
│
├── templates/              # Umumiy shablonlar (masalan, base.html)
├── static/                 # Umumiy statik fayllar (CSS, JS, rasmlar)
├── .env                    # Muhit o'zgaruvchilari (maxfiy saqlanadi)
├── .gitignore
├── manage.py
└── README.md
```
