FROM python:3.11.5-slim-bullseye
COPY ./Src /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]
