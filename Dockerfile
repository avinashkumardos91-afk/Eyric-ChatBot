FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

# Hugging Face Spaces requires apps to run on port 7860
EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "app.web_ui:app"]
