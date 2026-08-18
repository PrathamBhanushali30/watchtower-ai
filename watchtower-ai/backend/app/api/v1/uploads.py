from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.models import ModelUploadResponse
from app.utils.validators import allowed_file, compute_sha256_bytes, mime_matches, get_extension
from app.services.storage import upload_bytes
from app.db.session import get_db
from app.db import models as db_models
from app.core.config import settings

router = APIRouter()

@router.post("/models/upload", response_model=ModelUploadResponse)
async def upload_model(
    file: UploadFile = File(...),
    framework: str = "sklearn",
    owner_id: str = None,
    db: Session = Depends(get_db)
):
    filename = file.filename
    if not allowed_file(filename):
        raise HTTPException(status_code=400, detail="File type not allowed.")

    content = await file.read()
    if not mime_matches(content, filename):
        # we keep it permissive for binary model files but check basic mime
        raise HTTPException(status_code=400, detail="File mime mismatch or corrupted file.")

    sha = compute_sha256_bytes(content)
    key = f"{owner_id}/{sha}{get_extension(filename)}"

    # store in S3/MinIO
    try:
        artifact_s3_uri = upload_bytes(bucket=settings.S3_BUCKET, key=key, data=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {e}")

    # Save metadata in DB
    model_record = db_models.ModelArtifact(
        name=filename,
        owner_id=owner_id or "unknown",
        framework=framework,
        artifact_path=artifact_s3_uri,
        sha256=sha,
        metadata={}
    )
    db.add(model_record)
    db.commit()
    db.refresh(model_record)

    return ModelUploadResponse(model_id=model_record.id, name=model_record.name, status=model_record.status, message="Uploaded and registered.")
