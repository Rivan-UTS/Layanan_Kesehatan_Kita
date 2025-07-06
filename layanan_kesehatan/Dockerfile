# Gunakan image python resmi
FROM python:3.10

# Set working directory
WORKDIR /app

# Salin semua file
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
