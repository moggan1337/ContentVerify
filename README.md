# ContentVerify

Deepfake detection API for images and videos using FastAPI.

## Features

- **Image Analysis**: Detects manipulation in JPEG, PNG, WebP, GIF, and BMP images
- **Video Analysis**: Analyzes MP4, AVI, MOV, MKV, and WebM videos frame by frame
- **Multiple Techniques**: Combines ELA, frequency analysis, noise patterns, histogram analysis, and compression artifacts
- **REST API**: FastAPI-based API for easy integration

## Installation

```bash
# Clone the repository
git clone https://github.com/moggan1337/ContentVerify.git
cd ContentVerify

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Start the API Server

```bash
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

Or directly:

```bash
cd src
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "detector_ready": true,
  "version": "1.0.0"
}
```

#### Image Detection
```bash
POST /detect/image
Content-Type: multipart/form-data

Body: file (image file)
```

Example:
```bash
curl -X POST "http://localhost:8000/detect/image" \
  -F "file=@/path/to/image.jpg"
```

Response:
```json
{
  "filename": "image.jpg",
  "is_deepfake": false,
  "confidence": 23.45,
  "method": "frequency",
  "verdict": "AUTHENTIC",
  "confidence_level": "low",
  "details": {
    "ela_score": 0.12,
    "frequency_score": 0.23,
    "noise_score": 0.18,
    "histogram_score": 0.15,
    "compression_score": 0.25,
    "image_size": [1920, 1080],
    "image_mode": "RGB"
  }
}
```

#### Video Detection
```bash
POST /detect/video
Content-Type: multipart/form-data

Body: 
  - file (video file)
  - sample_frames (optional, default: 10, max: 30)
```

Example:
```bash
curl -X POST "http://localhost:8000/detect/video" \
  -F "file=@/path/to/video.mp4" \
  -F "sample_frames=15"
```

Response:
```json
{
  "filename": "video.mp4",
  "is_deepfake": true,
  "confidence": 67.82,
  "method": "video_analysis",
  "verdict": "DEEPFAKE",
  "confidence_level": "high",
  "details": {
    "total_frames": 300,
    "fps": 30.0,
    "frames_analyzed": 15,
    "frame_scores": [...],
    "variance": 0.12,
    "video_score": 0.68
  }
}
```

## Detection Methods

ContentVerify uses multiple analysis techniques:

1. **Error Level Analysis (ELA)**: Detects inconsistencies in compression artifacts
2. **Frequency Domain Analysis**: Uses DCT to detect unusual high-frequency patterns typical of GAN-generated content
3. **Noise Pattern Analysis**: Identifies inconsistent noise levels across the image
4. **Histogram Analysis**: Detects unusual color distributions
5. **Compression Artifact Analysis**: Examines inconsistencies in JPEG compression patterns

## Confidence Levels

| Level | Score Range |
|-------|-------------|
| very_low | 0-20% |
| low | 20-40% |
| medium | 40-60% |
| high | 60-80% |
| very_high | 80-100% |

## Configuration

Adjust the detection threshold in `src/detector.py`:

```python
detector = DeepfakeDetector(threshold=0.5)  # Default: 0.5
```

Lower values = more sensitive (more false positives)
Higher values = less sensitive (more false negatives)

## Development

### Run Tests

```bash
pytest tests/ -v
```

### Project Structure

```
ContentVerify/
├── src/
│   ├── __init__.py
│   ├── api.py          # FastAPI application
│   └── detector.py     # Detection algorithms
├── tests/
│   ├── __init__.py
│   └── test_detector.py
├── requirements.txt
└── README.md
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
