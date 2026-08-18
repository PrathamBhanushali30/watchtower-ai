# SQLAlchemy models
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="developer")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelArtifact(Base):
    __tablename__ = "models"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    framework = Column(String, nullable=False)
    artifact_path = Column(String, nullable=False)   # s3://bucket/...
    sha256 = Column(String, nullable=False)
    status = Column(String, default="registered")   # registered/active/quarantined
    meta_info = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
