WatchTower AI

WatchTower AI is a security-focused backend foundation for managing and securely registering machine-learning model artifacts. The project is designed with an emphasis on ML security, artifact integrity, controlled storage, API security, and containerized deployment.

The current implementation provides a FastAPI-based API with PostgreSQL metadata storage and MinIO/S3-compatible object storage. It also includes Docker Compose orchestration and a GitHub Actions security/CI pipeline.

Project status: Prototype / development foundation.
The repository currently implements the model-artifact registration and storage layer; advanced ML security analysis, model scanning, inference monitoring, and production-grade authentication/authorization are intended future components.

Key Features

FastAPI REST API

Health-check endpoint

User registration

Machine-learning model artifact upload

Automatic model artifact registration

Model Artifact Management

Supports:

.pkl

.joblib

.h5

.pt

.onnx

SHA-256 hashing for uploaded artifacts

Artifact metadata stored in PostgreSQL

Binary artifacts stored in MinIO/S3-compatible object storage

Security Controls

Password hashing using bcrypt

JWT token utilities

File-extension validation

MIME-type validation

SHA-256 integrity hashing

Private object-storage uploads

Bandit security scanning in CI

Trivy container-image scanning

Containerized Architecture

FastAPI backend

PostgreSQL database

MinIO object storage

Docker Compose for local deployment

CI Pipeline

Python dependency installation

Bandit security scan

Pytest execution

Docker image build

Trivy vulnerability scan

Architecture

                    ┌─────────────────────────┐
                    │       Client / User     │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP / REST
                                 ▼
                    ┌─────────────────────────┐
                    │       FastAPI API       │
                    │     WatchTower API      │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
        ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
        │   PostgreSQL   │ │    MinIO     │ │ Security / CI │
        │                │ │  S3 Storage  │ │               │
        │ Users          │ │ Model files  │ │ Bandit        │
        │ Model metadata │ │ Artifacts    │ │ Trivy         │
        └────────────────┘ └──────────────┘ └───────────────┘

Model Upload Flow

Model File
    │
    ▼
FastAPI Upload Endpoint
    │
    ├── Validate file extension
    │
    ├── Validate MIME type
    │
    ├── Calculate SHA-256
    │
    ├── Upload artifact to MinIO
    │
    └── Register metadata in PostgreSQL
                    │
                    ▼
             Model Artifact
              Registered

Technology Stack

Component

Technology

Backend

Python 3.10

API Framework

FastAPI

API Server

Uvicorn

Database

PostgreSQL 14

ORM

SQLAlchemy

Object Storage

MinIO / S3

Object Storage SDK

Boto3

Authentication Utilities

JWT / Passlib

Password Hashing

bcrypt

File Validation

python-magic

Containerization

Docker

Local Orchestration

Docker Compose

CI/CD

GitHub Actions

Security Scanning

Bandit + Trivy

Testing

Pytest

Project Structure

watchtower-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── models.py
│   │   │       ├── uploads.py
│   │   │       └── users.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   │
│   │   ├── services/
│   │   │   └── storage.py
│   │   │
│   │   ├── utils/
│   │   │   └── validators.py
│   │   │
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
└── README.md

Prerequisites

Install the following before running the project:

Docker

Docker Compose

Git

For running the backend directly without Docker:

Python 3.10

PostgreSQL

MinIO

libmagic / libmagic1

Quick Start with Docker Compose

1. Clone the repository

git clone <your-repository-url>
cd watchtower-ai

2. Start the services

docker compose up --build

This starts:

WatchTower API → http://localhost:8000

PostgreSQL → localhost:5432

MinIO API → http://localhost:9000

3. Check the API

Open:

http://localhost:8000/health

Expected response:

{
  "status": "ok"
}

4. Open Swagger API documentation

Visit:

http://localhost:8000/docs

FastAPI automatically provides an interactive Swagger UI.

Docker Services

API

The FastAPI backend is built from:

backend/Dockerfile

The API listens on:

0.0.0.0:8000

PostgreSQL

The development database uses:

Database: watchtower
Username: watchtower
Password: watchpass
Port: 5432

MinIO

The development object store uses:

Endpoint: http://localhost:9000
Username: minioadmin
Password: minioadmin
Bucket: models

These credentials are development defaults only and must be replaced before production deployment.

API Endpoints

Health Check

GET /health

Example:

curl http://localhost:8000/health

User Registration

POST /api/v1/users/register

Example request:

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "StrongPassword123!"
}

The password is hashed before being stored in the database.

Model Upload

The model-upload API accepts supported ML model artifacts and registers them in the system.

Supported extensions:

.pkl
.joblib
.h5
.pt
.onnx

The upload workflow:

Validate file extension.

Read the uploaded artifact.

Validate the detected MIME type.

Calculate SHA-256.

Store the artifact in MinIO/S3.

Store artifact metadata in PostgreSQL.

Return the registered model ID.

Example request:

curl -X POST \
  "http://localhost:8000/api/v1/models/upload?framework=onnx&owner_id=<USER_ID>" \
  -F "file=@model.onnx"

Example response:

{
  "model_id": "<MODEL_ID>",
  "name": "model.onnx",
  "status": "registered",
  "message": "Uploaded and registered."
}

Model Artifact Integrity

Every uploaded model is hashed using SHA-256.

Conceptually:

Model File
    │
    ▼
SHA-256
    │
    ▼
Unique Artifact Hash
    │
    ├── Used in storage key
    │
    └── Stored in PostgreSQL

This provides an integrity identifier that can later be used for:

Artifact verification

Duplicate detection

Version tracking

Audit trails

Tamper detection

Database Model

Users

The users table stores:

User ID

Email

Full name

Password hash

Role

Creation timestamp

Model Artifacts

The models table stores:

Model ID

Model filename

Owner ID

ML framework

S3/MinIO artifact path

SHA-256 hash

Status

Metadata

Creation timestamp

Model status values currently include:

registered
active
quarantined

These states provide a foundation for a future model-security lifecycle.

Security Design

WatchTower AI is intended to become a security-oriented ML artifact management platform.

The current codebase includes several security mechanisms.

Password Security

Passwords are not stored directly.

Plain Password
      │
      ▼
bcrypt
      │
      ▼
Password Hash
      │
      ▼
PostgreSQL

JWT Support

The project includes utilities for generating JWT access tokens using:

HS256

Token expiration is configurable.

File Validation

Uploaded artifacts are checked using:

File extension

MIME type

SHA-256 hashing

Object Storage

Model artifacts are stored through an S3-compatible interface using MinIO.

Static Analysis

GitHub Actions runs:

Bandit

against the backend source code.

Container Security

The CI pipeline builds the Docker image and scans it using:

Trivy

for high and critical vulnerabilities.

CI/CD Pipeline

The GitHub Actions workflow is located at:

.github/workflows/ci.yml

The pipeline performs:

Push / Pull Request
        │
        ▼
Install Python
        │
        ▼
Install Dependencies
        │
        ▼
Bandit Security Scan
        │
        ▼
Pytest
        │
        ▼
Build Docker Image
        │
        ▼
Trivy Container Scan

The workflow currently runs on:

main

pushes and pull requests.

Environment Configuration

Configuration is defined in:

backend/app/core/config.py

Important settings include:

PROJECT_NAME
API_V1_STR
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
S3_ENDPOINT
S3_ACCESS_KEY
S3_SECRET_KEY
S3_BUCKET
DATABASE_URL

For production, these values should be supplied through environment variables or a secrets manager rather than hard-coded development defaults.

Example:

SECRET_KEY=<strong-random-secret>
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:5432/<database>

S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY=<access-key>
S3_SECRET_KEY=<secret-key>
S3_BUCKET=models

Running Without Docker

Create a virtual environment:

python3.10 -m venv .venv

Activate it.

Linux/macOS:

source .venv/bin/activate

Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r backend/requirements.txt

Set the required environment variables and make sure PostgreSQL and MinIO are available.

Then run:

cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Testing

Run the test suite with:

pytest -q

Security analysis:

bandit -r backend/app

Container vulnerability scanning is performed automatically by the GitHub Actions workflow using Trivy.

Security Considerations

This repository is currently a development/prototype implementation. Before production use, the following should be addressed:

Replace default PostgreSQL and MinIO credentials.

Replace the default JWT secret.

Move secrets to a proper secret-management system.

Implement complete login/token issuance and token validation.

Add authentication and authorization dependencies to protected endpoints.

Enforce ownership checks for uploaded model artifacts.

Add upload-size limits.

Add stronger model-file validation.

Add malware and model-payload scanning.

Add model deserialization safety controls.

Add database migrations, preferably with Alembic.

Add comprehensive automated tests.

Add structured logging and audit logging.

Add rate limiting.

Add HTTPS/TLS for production deployments.

Add container hardening and least-privilege execution.

Add model lifecycle/version management.

Add quarantine and approval workflows.

Roadmap

The project can be extended toward a complete secure ML/MLOps security platform.

Phase 1 — Foundation

FastAPI backend

PostgreSQL integration

MinIO/S3 integration

Model artifact upload

SHA-256 artifact hashing

File validation

Docker Compose

CI pipeline

Bandit scanning

Trivy scanning

Phase 2 — Identity & Access

Login endpoint

JWT authentication flow

Role-based access control

Model ownership enforcement

Token refresh/revocation

API rate limiting

Phase 3 — AI/ML Security

Malicious model detection

Pickle/joblib security analysis

ONNX model inspection

Model metadata analysis

Dependency/package analysis

Model provenance tracking

Model integrity verification

Phase 4 — Threat Detection

Malware scanning

YARA integration

VirusTotal integration

Hybrid Analysis integration

Threat intelligence enrichment

IOC extraction

Risk scoring

Phase 5 — Security Operations

Security dashboard

Audit logs

Alert management

SIEM integration

Model quarantine

Security event correlation

Notifications

Phase 6 — Production Deployment

Kubernetes deployment

Secrets management

TLS

High availability

Observability

Prometheus/Grafana monitoring

Centralized logging

Production CI/CD

Security Architecture Vision

The long-term architecture can evolve into:

                    ┌──────────────────────┐
                    │       Developer      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   WatchTower API     │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Model Intake Layer   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
      ┌─────────────┐   ┌──────────────┐   ┌─────────────┐
      │ File/MIME   │   │ Hash &       │   │ Malware /   │
      │ Validation  │   │ Integrity    │   │ Model Scan  │
      └─────────────┘   └──────────────┘   └─────────────┘
             │                 │                  │
             └─────────────────┼──────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Risk Scoring Engine  │
                    └──────────┬───────────┘
                               │
                   ┌───────────┴───────────┐
                   ▼                       ▼
             ┌───────────┐          ┌─────────────┐
             │ Quarantine│          │ Approved    │
             │           │          │ Artifact    │
             └───────────┘          └──────┬──────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │ MinIO / S3  │
                                    └─────────────┘

Contributing

Fork the repository.

Create a feature branch.

git checkout -b feature/<feature-name>

Make your changes.

Run tests and security checks.

pytest -q
bandit -r backend/app

Commit your changes.

git commit -m "feat: add <feature>"

Push the branch and open a pull request.

Disclaimer

This project is intended for research, development, and security engineering purposes. Do not deploy the included development credentials or configuration directly in a production environment.

Author

Pratham Bhanushali

M.Tech — Artificial Intelligence & Data Science
Specialization: Cybersecurity

Project: WatchTower AI

Areas of focus:

Cybersecurity

AI/ML Security

Secure MLOps

Threat Detection

Model Security

Security Automation
