# ContentVerify

<p align="center">
  <img src="https://img.shields.io/badge/Deepfake-Detection-FF6B6B?style=for-the-badge&logo=shield&logoColor=white" alt="AI">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" alt="PRs Welcome">
</p>

> 🔍 **Deepfake & Content Authenticity Detector** — AI-powered verification engine for images, videos, and audio. Detect manipulated content, verify authenticity, and establish provenance with blockchain timestamping.

## About

ContentVerify is a comprehensive content authentication platform that uses advanced AI models to detect manipulated media and verify the authenticity of digital content. Designed for journalists, fact-checkers, brands, and platforms, it provides confidence scores, provenance tracking, and immutable verification certificates.

**Who it's for:**
- Journalists and fact-checkers verifying media authenticity
- Brands protecting against fraudulent use of their content
- Social platforms implementing content moderation
- Legal teams requiring evidence authentication
- Healthcare and finance sectors with strict media integrity requirements

## Features

### Detection Capabilities

| Feature | Description |
|---------|-------------|
| 🎭 **Face Swap Detection** | Identifies face replacement in videos (deepfakes) |
| 🖼️ **Image Manipulation** | Detects Photoshop, GAN-generated, and AI-synthesized images |
| 🔊 **Voice Clone Detection** | Identifies synthetic or cloned audio |
| 📝 **AI Text Detection** | Detects AI-generated text content |
| 📍 **EXIF Analysis** | Verifies metadata and geolocation data |
| 🎨 **Style Consistency** | Detects inconsistencies in artistic style |

### Verification System

| Feature | Description |
|---------|-------------|
| ✅ **Authenticity Score** | 0-100 confidence score for content authenticity |
| 📜 **Provenance Chain** | Full chain of custody tracking from origin |
| 🔗 **Blockchain Stamp** | Immutable verification record on blockchain |
| 📄 **Verification Certificate** | Downloadable official verification document |

### Analysis Types

| Type | Output |
|------|--------|
| **Image Analysis** | Manipulation detection, GAN fingerprinting, EXIF report |
| **Video Analysis** | Frame-by-face analysis, temporal consistency, deepfake score |
| **Audio Analysis** | Voice clone detection, synthesis markers, spectrogram analysis |
| **Text Analysis** | AI generation probability, writing style analysis |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      ContentVerify System                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      Input Processing                      │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │   │
│  │  │     Image     │ │     Video    │ │     Audio    │      │   │
│  │  │   Upload     │ │   Upload     │ │   Upload     │      │   │
│  │  │   (Multipart) │ │   (Chunks)   │ │   (Stream)   │      │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘      │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │   │
│  │  │   URL Fetch  │ │   Text Input │ │   EXIF Parse │      │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌────────────────────────────┴──────────────────────────────┐   │
│  │                    Detection Engine                        │   │
│  │  ┌──────────────────────────────────────────────────────┐ │   │
│  │  │                 AI Models Layer                       │ │   │
│  │  │                                                        │ │   │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │ │   │
│  │  │  │    Face     │ │    Image    │ │    Audio    │   │ │   │
│  │  │  │  Detector   │ │  Forensics  │ │  Analysis   │   │ │   │
│  │  │  │             │ │             │ │             │   │ │   │
│  │  │  │ • Meso4     │ │ • ELA       │ │ • WaveNet   │   │ │   │
│  │  │  │ • Xception  │ │ • Noise     │ │ • Spec.     │   │ │   │
│  │  │  │ • FaceSwap  │ │   Analysis  │ │   Analysis  │   │ │   │
│  │  │  │   CNN       │ │ • GAN       │ │ • Voice     │   │ │   │
│  │  │  │             │ │   Finger-   │ │   Clone     │   │ │   │
│  │  │  │             │ │   printing  │ │   Detector  │   │ │   │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘   │ │   │
│  │  │                                                        │ │   │
│  │  │  ┌─────────────┐ ┌─────────────┐                    │ │   │
│  │  │  │     NLP     │ │   Metadata   │                    │ │   │
│  │  │  │  AI Text    │ │   Analyzer   │                    │ │   │
│  │  │  │  Detector   │ │              │                    │ │   │
│  │  │  │             │ │ • EXIF       │                    │ │   │
│  │  │  │ • Transformer│ │ • Geolocation│                    │ │   │
│  │  │  │ • Bayesian  │ │ • Timestamp   │                    │ │   │
│  │  │  │   Detector │ │   Forensics  │                    │ │   │
│  │  │  └─────────────┘ └─────────────┘                    │ │   │
│  │  └──────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌────────────────────────────┴──────────────────────────────┐   │
│  │                  Verification Engine                       │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │   │
│  │  │   Confidence │ │  Provenance  │ │  Blockchain  │       │   │
│  │  │    Scoring   │ │    Tracker   │ │   Stamper    │       │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌────────────────────────────┴──────────────────────────────┐   │
│  │                      Output Layer                          │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  • Verification Report (JSON/PDF)                 │  │   │
│  │  │  • Authenticity Certificate                        │  │   │
│  │  │  • Blockchain Transaction Hash                      │  │   │
│  │  │  • Detailed Analysis Breakdown                      │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.11+ |
| **API Framework** | FastAPI 0.104, Pydantic v2, Uvicorn |
| **ML/AI** | TensorFlow 2.14, PyTorch 2.1, Transformers |
| **Computer Vision** | OpenCV, Pillow, scikit-image |
| **Audio Processing** | Librosa, Torchaudio, WaveNet |
| **NLP** | HuggingFace Transformers, spaCy |
| **Blockchain** | Ethereum (for stamping), Web3.py |
| **Storage** | PostgreSQL 15 (verification records), Redis 7 (cache) |
| **Queue** | Celery, RabbitMQ |

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (for verification records)
- Redis 7+ (for caching)
- FFmpeg (for video/audio processing)
- 8GB+ RAM recommended

### Steps

```bash
# Clone the repository
git clone https://github.com/moggan1337/ContentVerify.git
cd ContentVerify

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download AI models
python scripts/download_models.py

# Copy and configure environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Start API server
uvicorn api.main:app --reload
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `REDIS_URL` | Redis connection string | ✅ |
| `BLOCKCHAIN_RPC_URL` | Ethereum RPC endpoint | Optional |
| `BLOCKCHAIN_PRIVATE_KEY` | Private key for stamping | Optional |
| `API_KEY` | API authentication key | Optional |

## Quick Start

### Verify an Image

```python
from contentverify import Verifier

verifier = Verifier()

# Verify image authenticity
result = verifier.verify_image(
    image_path="path/to/image.jpg",
    options={"check_exif": True, "check_gan": True}
)

print(result)
```

### Response Format

```json
{
  "verification_id": "ver_abc123xyz",
  "status": "complete",
  "content_type": "image",
  "authenticity_score": 23,
  "confidence": 0.94,
  "is_authentic": false,
  "verdict": "LIKELY_MANIPULATED",
  "analysis": {
    "manipulation_detected": true,
    "gan_generated_probability": 0.78,
    "exif tampering": false,
    "suspicious_elements": [
      {"type": "face_inconsistency", "confidence": 0.89, "location": "region_1"}
    ]
  },
  "provenance": {
    "source": "upload",
    "first_seen": "2024-11-01T10:30:00Z",
    "checks_performed": ["exif", "ela", "noise", "gan_fingerprint"]
  },
  "certificate_url": "https://api.contentverify.io/certs/ver_abc123xyz.pdf",
  "blockchain_stamp": {
    "tx_hash": "0x1234...5678",
    "network": "ethereum",
    "timestamp": "2024-11-10T15:45:00Z"
  },
  "created_at": "2024-11-10T15:45:23Z"
}
```

### Verify a Video

```python
result = verifier.verify_video(
    video_path="path/to/video.mp4",
    options={"check_faceswap": True, "check_voiceclone": True}
)
```

### Verify Text Content

```python
result = verifier.verify_text(
    text="Your content here...",
    options={"check_ai_generation": True}
)
```

### Batch Verification

```python
results = verifier.verify_batch([
    {"type": "image", "path": "image1.jpg"},
    {"type": "video", "path": "video1.mp4"},
    {"type": "text", "content": "Sample text to verify"}
])
```

## API Reference

### Verification Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/verify/image` | Verify image authenticity |
| `POST` | `/api/v1/verify/video` | Verify video authenticity |
| `POST` | `/api/v1/verify/audio` | Verify audio authenticity |
| `POST` | `/api/v1/verify/text` | Verify text authenticity |
| `POST` | `/api/v1/verify/batch` | Batch verification |

### Results

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/verifications/:id` | Get verification result |
| `GET` | `/api/v1/verifications/:id/certificate` | Download verification certificate |
| `GET` | `/api/v1/verifications/:id/report` | Get detailed analysis report |

### Analysis Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/analyze/exif` | Extract and analyze EXIF data |
| `POST` | `/api/v1/analyze/gan-fingerprint` | Detect GAN generation artifacts |
| `POST` | `/api/v1/analyze/metadata` | Analyze file metadata |

## Detection Models

### Face Swap Detection
- **Meso4**: Fast face analysis network for initial screening
- **Xception**: Deep residual network for detailed face analysis
- **FaceSwap CNN**: Specialized network trained on face swap datasets

### Image Forensics
- **Error Level Analysis (ELA)**: Detects editing through compression artifacts
- **Noise Consistency Analysis**: Identifies inconsistent noise patterns
- **GAN Fingerprinting**: Detects GAN-specific artifacts in generated images

### Audio Analysis
- **WaveNet-based Detector**: Identifies synthetic speech patterns
- **Spectrogram Analysis**: Detects voice cloning artifacts
- **Prosody Analysis**: Verifies natural speech rhythm and intonation

### Text Analysis
- **Transformer Classifier**: Detects AI-generated text patterns
- **Bayesian Detector**: Statistical analysis of writing style

## Contributing

Contributions are welcome! Please follow these steps:

```bash
# Fork the repository
git clone https://github.com/<your-username>/ContentVerify.git

# Create virtual environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Create feature branch
git checkout -b feature/detection-improvement

# Make changes, commit, and push
git commit -m "Improve: detection accuracy for face swap"
git push origin feature/detection-improvement
```

### Development Guidelines

- Use type hints for all function signatures
- Follow PEP 8 style guide
- Add tests for new detection models
- Document model accuracy metrics
- Update API documentation for new endpoints

## License

MIT License — See [LICENSE](LICENSE)

Copyright © 2024 ContentVerify Contributors

---

<p align="center">
  <sub>Trust but verify — powered by AI</sub>
</p>
