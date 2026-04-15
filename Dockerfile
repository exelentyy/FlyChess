# Wybieramy obraz Pythona
FROM python:3.10-slim

# Instalujemy zależności systemowe (często potrzebne dla PyChess/bibliotek szachowych)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Ustawiamy folder roboczy
WORKDIR /app

# Kopiujemy listę bibliotek i instalujemy je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę plików projektu
COPY . .

# Port, na którym działa PyChess (zmień jeśli używasz innego niż 8080)
EXPOSE 8080

# Komenda startowa (dostosuj do swojego głównego pliku, np. main.py lub app.py)
CMD ["python", "pychess"]
