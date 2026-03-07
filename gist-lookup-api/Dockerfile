# --------------------
# Builder stage
# --------------------
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --------------------
# Final stage – minimal image
# --------------------
FROM python:3.12-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy minimal source code
COPY src/ ./src/

EXPOSE 8080

# Run with uvicorn (production ready server)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--no-access-log"]