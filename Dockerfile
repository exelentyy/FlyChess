FROM python:3.10-slim

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Tworzymy użytkownika (Hugging Face nie lubi roota)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

WORKDIR /home/user/app

# Kopiujemy requirements i instalujemy biblioteki
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Kopiujemy resztę kodu
COPY --chown=user . .

# PORT MUSI BYĆ 7860
EXPOSE 7860

# Komenda startowa - upewnij się, że Twoja aplikacja 
# przyjmuje argument --port lub nasłuchuje na 7860 domyślnie
CMD ["python", "main.py", "--port", "7860"]

