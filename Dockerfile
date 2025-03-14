FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

RUN node -v && npm -v

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY theme/static_src/package.json ./theme/static_src/

WORKDIR /app/theme/static_src
RUN npm install -g yarn && yarn install


WORKDIR /app
COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py scrape_products
RUN python manage.py create_admin


RUN python manage.py tailwind build

RUN python manage.py collectstatic


EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=quickcart.settings
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "quickcart.wsgi:application"]