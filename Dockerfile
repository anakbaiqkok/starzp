FROM python:3.10-slim

# Update dan instal paket yang diperlukan
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg git neofetch apt-utils libmediainfo0v5 sqlite3 \
    libgl1-mesa-glx libglib2.0-0 libxml2-dev libxslt-dev sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Buat direktori kerja dan salin file yang diperlukan
WORKDIR /app

# Salin file requirements terlebih dahulu untuk memanfaatkan cache Docker
COPY requirements.txt .

# Instal dependensi Python
RUN pip3 install -U pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Salin skrip start dan buat bisa dieksekusi
COPY start.sh .
RUN chmod +x start.sh

# Terakhir, salin semua file aplikasi
COPY . .

# Set variabel lingkungan
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port yang dibutuhkan
EXPOSE 7860-8000


# Set entrypoint
ENTRYPOINT ["./start.sh"]