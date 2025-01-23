FROM python:3.10

WORKDIR /app

VOLUME '/app' '/app/files'

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "streamlit", "run" ]

CMD ["poupa_app.py"]