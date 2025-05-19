FROM python:3.9-slim AS builder
WORKDIR /usr/src/app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY *.py /app/
ENV PATH="/opt/venv/bin:$PATH"
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
