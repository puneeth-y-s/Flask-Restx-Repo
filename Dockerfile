FROM python:3.9-alpine3.18
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP application.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
