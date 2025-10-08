# 1-bosqich: Bog'liqliklarni o'rnatish
FROM python:3.11-slim-bookworm AS builder

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
RUN python3 -m pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# 2-bosqich: Asosiy image'ni yaratish
FROM python:3.11-slim-bookworm

WORKDIR /app

# Bog'liqliklarni builder'dan ko'chirish
COPY --from=builder /app/wheels /wheels
COPY --from=builder /usr/local/bin/pip /usr/local/bin/pip
RUN python3 -m pip install --no-cache /wheels/*

# Loyiha kodini ko'chirish
COPY . .

# Xavfsizlik uchun alohida foydalanuvchi yaratish
RUN useradd -ms /bin/bash appuser
USER appuser

EXPOSE 8000

# Gunicorn'ni ishga tushirish (docker-compose da aniqroq ko'rsatiladi)
CMD ["/usr/local/bin/gunicorn", "aml.wsgi:application", "--bind", "0.0.0.0:8000"]

