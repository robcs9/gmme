# FROM python:3.9
FROM python:alpine3.21

WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app
# COPY . /code/app
COPY . .

# CMD ["fastapi", "run", "app/main.py", "--port", "8123"]
CMD ["fastapi", "run", "main.py", "--port", "8123"]

EXPOSE 8123

# If running behind a proxy like Nginx or Traefik add --proxy-headers e.g.:
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]