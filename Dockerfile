FROM gateguardai/rtsp_recorder:v1

WORKDIR /app

COPY . /app

CMD ["streamlit", "run", "recorder.py", "--server.port", "3000"]
