# Use a lightweight official Python image
FROM python:3.11-slim

# Install system utilities (curl for potential healthchecks)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user with UID 1000 (Hugging Face Spaces requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Create and set the working directory
WORKDIR $HOME/app

# Copy dependencies first to leverage Docker layer caching
COPY --chown=user backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the backend and frontend source directories
COPY --chown=user backend/ ./backend
COPY --chown=user frontend/ ./frontend

# Expose port 7860 (Hugging Face Spaces routes public traffic to this port)
EXPOSE 7860

# Run the FastAPI server on host 0.0.0.0 and port 7860
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
