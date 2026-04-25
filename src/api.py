"""
ContentVerify API

FastAPI-based REST API for deepfake content detection.
"""

import io
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.detector import DeepfakeDetector, DetectionResult


# Global detector instance
detector: Optional[DeepfakeDetector] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup."""
    global detector
    detector = DeepfakeDetector(threshold=0.5)
    yield
    detector = None


app = FastAPI(
    title="ContentVerify API",
    description="Deepfake detection API for images and videos",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the status of the API and detector.
    """
    return {
        "status": "healthy",
        "detector_ready": detector is not None,
        "version": "1.0.0"
    }


@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    """
    Detect deepfake in an uploaded image.
    
    Accepts: JPEG, PNG, WebP, GIF, BMP
    
    Returns:
        Detection result with confidence score and analysis details
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}"
        )
    
    # Check file size (max 50MB)
    max_size = 50 * 1024 * 1024
    contents = await file.read()
    
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {max_size // (1024*1024)}MB"
        )
    
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    try:
        result = detector.detect_image(contents)
        return format_result(result, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...), sample_frames: int = 10):
    """
    Detect deepfake in an uploaded video.
    
    Accepts: MP4, AVI, MOV, MKV, WebM
    
    Args:
        file: Video file upload
        sample_frames: Number of frames to analyze (default: 10)
    
    Returns:
        Detection result with confidence score and per-frame analysis
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    # Validate file type
    allowed_types = [
        "video/mp4", "video/avi", "video/quicktime", 
        "video/x-matroska", "video/webm", "video/x-msvideo"
    ]
    
    # Some clients send different MIME types
    filename_lower = file.filename.lower() if file.filename else ""
    is_allowed_ext = any(
        filename_lower.endswith(ext) 
        for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    )
    
    if file.content_type not in allowed_types and not is_allowed_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}"
        )
    
    # Check file size (max 200MB)
    max_size = 200 * 1024 * 1024
    contents = await file.read()
    
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {max_size // (1024*1024)}MB"
        )
    
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    # Limit sample frames
    sample_frames = min(max(sample_frames, 1), 30)
    
    try:
        result = detector.detect_video(contents, sample_frames=sample_frames)
        return format_result(result, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


def format_result(result: DetectionResult, filename: str) -> dict:
    """Format detection result for API response."""
    return {
        "filename": filename,
        "is_deepfake": result.is_deepfake,
        "confidence": round(result.confidence, 2),
        "method": result.method,
        "details": result.details,
        "verdict": "DEEPFAKE" if result.is_deepfake else "AUTHENTIC",
        "confidence_level": get_confidence_level(result.confidence)
    }


def get_confidence_level(confidence: float) -> str:
    """Convert confidence score to human-readable level."""
    if confidence >= 80:
        return "very_high"
    elif confidence >= 60:
        return "high"
    elif confidence >= 40:
        return "medium"
    elif confidence >= 20:
        return "low"
    else:
        return "very_low"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
