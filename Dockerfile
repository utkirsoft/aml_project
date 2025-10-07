<<<<<<< HEAD
# 1-bosqich: Bog'liqliklarni o'rnatish
FROM python:3.10-slim-buster AS builder
=======
# 1-bosqich Bog'liqliklarni o'rnatish
FROM python:3.11-slim-bookworm AS builder
>>>>>>> c855b9f (dockervoy)

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Kerakli paketlarni o'rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    vim \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pyhon3 -m pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

<<<<<<< HEAD
# 2-bosqich: Asosiy image'ni yaratish
FROM python:3.10-slim-buster
=======
# 2-bosqich Asosiy image'ni yaratish
FROM python:3.10-slim-bookworm
>>>>>>> c855b9f (dockervoy)

WORKDIR /app

# Bog'liqliklarni builder'dan ko'chirish
<<<<<<< HEAD
COPY --from-builder /app/wheels /wheels
COPY --from-builder /usr/local/bin/pip /usr/local/bin/pip
RUN pip install --no-cache /wheels/*
=======
COPY --from=builder /app/wheels wheels
COPY --from=builder /usr/local/bin/pip /usr/local/bin/pip
RUN python3 -m pip install --no-cache /wheels/*
>>>>>>> c855b9f (dockervoy)

# Loyiha kodini ko'chirish
COPY . .

# Xavfsizlik uchun alohida foydalanuvchi yaratish
RUN useradd -ms /bin/bash appuser
USER appuser

EXPOSE 8000

# Gunicorn'ni ishga tushirish (docker-compose da aniqroq ko'rsatiladi)
CMD ["gunicorn", "aml.wsgi:application", "--bind", "0.0.0.0:8000"]

