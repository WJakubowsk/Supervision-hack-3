FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8501

CMD ["streamlit", "run", "--server.port", "8501", "app/app.py"]

