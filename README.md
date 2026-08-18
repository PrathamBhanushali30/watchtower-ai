# 🗼 WatchTower AI
> **A security-focused backend foundation for managing, validating, and securely registering machine-learning model artifacts.**

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Security](https://img.shields.io/badge/Security-Bandit%20%7C%20Trivy-red)

WatchTower AI is designed with an emphasis on ML security, artifact integrity, controlled storage, API security, and containerized deployment. It provides a robust FastAPI-based layer with PostgreSQL metadata storage, S3-compatible object storage (MinIO), Docker Compose orchestration, and a GitHub Actions DevSecOps pipeline.

**Project Status:** 🚧 *Prototype / Development Foundation*  
*Currently implements the model-artifact registration and storage layer. Advanced ML security analysis, inference monitoring, and production-grade auth are on the roadmap.*

---

## ✨ Key Features

### 📦 Model Artifact Management
*   **Broad Framework Support:** Native support for `.pkl`, `.joblib`, `.h5`, `.pt`, and `.onnx`.
*   **Cryptographic Integrity:** Automated SHA-256 hashing for all uploaded artifacts.
*   **Structured Metadata:** Artifact metadata rigorously tracked in PostgreSQL.
*   **Secure Blob Storage:** Binary artifacts isolated in MinIO/S3-compatible object storage.

### 🛡️ Security Controls
*   **Authentication:** Password hashing using `bcrypt` and JWT token utilities.
*   **Validation:** Strict file-extension and MIME-type validation (`python-magic`).
*   **Secure Storage:** Private object-storage uploads preventing unauthorized direct access.
*   **DevSecOps Pipeline:** Automated `Bandit` security scanning and `Trivy` container-image vulnerability scanning in CI.

### 🐳 Containerized Architecture
*   Fully containerized FastAPI backend, PostgreSQL database, and MinIO object storage using Docker Compose for seamless local deployment.

---

## 🏗️ Architecture

### System Topology
```text
                    ┌─────────────────────────┐
                    │       Client / User     │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP / REST
                                 ▼
                    ┌─────────────────────────┐
                    │        FastAPI API      │
                    │      WatchTower API     │
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
