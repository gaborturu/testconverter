FROM python:3.6-slim-buster
WORKDIR /home
EXPOSE 8080
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run app.py --server.port 8080
