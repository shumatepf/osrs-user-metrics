FROM python:3.8.10

COPY ./requirements.txt /osrs/requirements.txt

WORKDIR /osrs


RUN pip install -r requirements.txt

COPY ./osrs /osrs

CMD ["python3", "-m", "flask", "--app", ".", "run", "-h", "0.0.0.0"]