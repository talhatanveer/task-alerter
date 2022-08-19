FROM python:3.9

WORKDIR /app

# RUN python3 -m pip install pipenv
# COPY Pipfile* .

# RUN python3 -m pipenv lock --keep-outdated -r > requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

CMD ["python3", "app.py"]