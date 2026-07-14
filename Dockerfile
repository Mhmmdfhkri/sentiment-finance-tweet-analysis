FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /code

# Copy requirements dahulu agar proses build cepat memanfaatkan cache
COPY ./requirements.txt /code/requirements.txt

# Install library Python
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Buat user baru dengan ID 1000 untuk keamanan Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Salin semua file dari lokal komputer ke dalam container
COPY --chown=user . $HOME/app

# Ekspos port default Hugging Face (7860)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]