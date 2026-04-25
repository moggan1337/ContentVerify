# ContentVerify

<p align="center">
  <img src="https://img.shields.io/badge/Deepfake-Detection-FF6B6B?style=for-the-badge&logo=shield&logoColor=white" alt="AI">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 🔍 **Deepfake & Content Authenticity Detector** - AI-powered verification for images and videos. Detects manipulated content, verifies authenticity.

## ✨ Features

### Detection
- 🎭 **Face Swap** - Detect face replacement in videos
- 🖼️ **Image Manipulation** - Detect Photoshop, GAN-generated images
- 🔊 **Voice Clone** - Audio deepfake detection
- 📝 **Text AI** - Detect AI-generated text
- 📍 **EXIF Analysis** - Verify metadata and origin

### Verification
- ✅ **Authenticity Score** - 0-100 confidence score
- 📜 **Provenance Chain** - Track content origin
- 🔗 **Blockchain Stamp** - Immutable verification record
- 📄 **Certificate** - Downloadable verification certificate

## 📦 Installation

```bash
git clone https://github.com/moggan1337/ContentVerify.git
cd ContentVerify
pip install -r requirements.txt
python scripts/download_models.py
uvicorn api.main:app --reload
```

## 📄 License

MIT License
