# 1-bosqich Bog'liqliklarni o'rnatish
FROM python3.10-slim-buster AS builder

WORKDIR app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Kerakli paketlarni o'rnatish
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir appwheels -r requirements.txt

# 2-bosqich Asosiy image'ni yaratish
FROM python3.10-slim-buster

WORKDIR app

# Bog'liqliklarni builder'dan ko'chirish
COPY --from=builder appwheels wheels
COPY --from=builder usrlocalbinpip usrlocalbinpip
RUN pip install --no-cache wheels

# Loyiha kodini ko'chirish
COPY . .

# Xavfsizlik uchun alohida foydalanuvchi yaratish
RUN useradd -ms binbash appuser
USER appuser

EXPOSE 8000

# Gunicorn'ni ishga tushirish (docker-compose da aniqroq ko'rsatiladi)
CMD [gunicorn, aml.wsgiapplication, --bind, 0.0.0.08000]