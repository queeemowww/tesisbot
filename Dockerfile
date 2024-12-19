FROM python:latest
WORKDIR /tesisbot
ADD . .
RUN pip install -r requirements.txt
CMD ["python", "app/main.py"]