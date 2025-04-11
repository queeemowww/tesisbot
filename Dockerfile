FROM ubuntu:latest
FROM python:latest
WORKDIR /tesisbot
ADD . .
RUN pip install -r requirements.txt
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo dpkg -i google-chrome-stable_current_amd64.deb
CMD ["python", "app/main.py"]