# Protein Calculator container image (automation#356).
#
# Built on the VPS by the automation container_service role (external-repo mode)
# and pushed to ECR. The async SQLite DB lives on a bind-mounted /data volume;
# its location comes from PROTEIN_DATABASE_URL in the environment. Stateless
# image otherwise.

FROM python:3.12-slim AS runtime
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=5s \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/')"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
