# Backend image
FROM python:3.10-slim AS backend

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .

# Frontend image
FROM node:20-alpine AS frontend

WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build

# Production container
FROM python:3.10-slim

WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/frontend

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
