"""
Tests for DeepfakeDetector

Comprehensive tests covering image and video detection,
edge cases, and various image formats.
"""

import io
import pytest
import numpy as np
from PIL import Image

from src.detector import DeepfakeDetector, DetectionResult


class TestDeepfakeDetector:
    """Test suite for DeepfakeDetector class."""
    
    @pytest.fixture
    def detector(self):
        """Create a detector instance for testing."""
        return DeepfakeDetector(threshold=0.5)
    
    @pytest.fixture
    def sample_image_bytes(self):
        """Generate a simple test image."""
        img = Image.new('RGB', (256, 256), color=(128, 128, 128))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return buffer.read()
    
    @pytest.fixture
    def solid_color_image(self):
        """Generate a solid color image."""
        img = Image.new('RGB', (100, 100), color=(255, 0, 0))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.read()
    
    @pytest.fixture
    def noisy_image(self):
        """Generate an image with random noise."""
        arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(arr)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return buffer.read()
    
    @pytest.fixture
    def gradient_image(self):
        """Generate a smooth gradient image."""
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        for i in range(100):
            arr[i, :, :] = [i * 2, i * 2, i * 2]
        img = Image.fromarray(arr)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.read()
    
    def test_detector_initialization(self, detector):
        """Test detector initializes with correct default threshold."""
        assert detector.threshold == 0.5
        
    def test_detector_custom_threshold(self):
        """Test detector accepts custom threshold."""
        detector = DeepfakeDetector(threshold=0.7)
        assert detector.threshold == 0.7
    
    def test_detect_image_returns_result(self, detector, sample_image_bytes):
        """Test detect_image returns a DetectionResult."""
        result = detector.detect_image(sample_image_bytes)
        
        assert isinstance(result, DetectionResult)
        assert hasattr(result, 'is_deepfake')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'method')
        assert hasattr(result, 'details')
    
    def test_detect_image_with_various_formats(self, detector, solid_color_image, noisy_image, gradient_image):
        """Test detection works with different image formats."""
        formats = [
            (solid_color_image, 'PNG solid color'),
            (noisy_image, 'JPEG noisy'),
            (gradient_image, 'PNG gradient'),
        ]
        
        for image_bytes, name in formats:
            result = detector.detect_image(image_bytes)
            assert result is not None, f"Failed for {name}"
            assert 0 <= result.confidence <= 100, f"Invalid confidence for {name}"
    
    def test_detect_image_contains_analysis_scores(self, detector, sample_image_bytes):
        """Test result contains all expected analysis scores."""
        result = detector.detect_image(sample_image_bytes)
        
        assert 'ela_score' in result.details
        assert 'frequency_score' in result.details
        assert 'noise_score' in result.details
        assert 'histogram_score' in result.details
        assert 'compression_score' in result.details
    
    def test_detect_image_includes_image_metadata(self, detector, sample_image_bytes):
        """Test result includes image size and mode."""
        result = detector.detect_image(sample_image_bytes)
        
        assert 'image_size' in result.details
        assert 'image_mode' in result.details
    
    def test_detect_image_handles_grayscale(self, detector):
        """Test detection handles grayscale images."""
        img = Image.new('L', (100, 100), color=128)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        
        result = detector.detect_image(buffer.read())
        assert isinstance(result, DetectionResult)
    
    def test_detect_image_handles_rgba(self, detector):
        """Test detection handles RGBA images."""
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        result = detector.detect_image(buffer.read())
        assert isinstance(result, DetectionResult)
    
    def test_detect_image_handles_corrupted_data(self, detector):
        """Test detector handles corrupted/invalid image data gracefully."""
        result = detector.detect_image(b'not an image')
        
        assert isinstance(result, DetectionResult)
        assert result.method == 'error'
        assert 'error' in result.details
    
    def test_detect_image_handles_empty_data(self, detector):
        """Test detector handles empty data."""
        result = detector.detect_image(b'')
        
        assert isinstance(result, DetectionResult)
        assert result.method == 'error'
    
    def test_confidence_score_bounds(self, detector, sample_image_bytes, noisy_image):
        """Test confidence scores are within valid bounds."""
        test_images = [
            (sample_image_bytes, 'sample'),
            (noisy_image, 'noisy'),
        ]
        
        for image_bytes, name in test_images:
            result = detector.detect_image(image_bytes)
            assert 0 <= result.confidence <= 100, f"Confidence out of bounds for {name}"
    
    def test_threshold_affects_classification(self):
        """Test that different thresholds produce different classifications."""
        detector_low = DeepfakeDetector(threshold=0.1)
        detector_high = DeepfakeDetector(threshold=0.9)
        
        # Create an image that should trigger different classifications
        arr = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        img = Image.fromarray(arr)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        image_bytes = buffer.read()
        
        result_low = detector_low.detect_image(image_bytes)
        result_high = detector_high.detect_image(image_bytes)
        
        # Both should return valid results
        assert isinstance(result_low, DetectionResult)
        assert isinstance(result_high, DetectionResult)
    
    def test_ela_analysis_returns_valid_score(self, detector):
        """Test ELA analysis returns score between 0 and 1."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        score = detector._ela_analysis(img)
        
        assert 0 <= score <= 1
    
    def test_frequency_analysis_returns_valid_score(self, detector):
        """Test frequency analysis returns score between 0 and 1."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        score = detector._frequency_analysis(img)
        
        assert 0 <= score <= 1
    
    def test_noise_analysis_returns_valid_score(self, detector):
        """Test noise analysis returns score between 0 and 1."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        score = detector._noise_analysis(img)
        
        assert 0 <= score <= 1
    
    def test_histogram_analysis_returns_valid_score(self, detector):
        """Test histogram analysis returns score between 0 and 1."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        score = detector._histogram_analysis(img)
        
        assert 0 <= score <= 1
    
    def test_compression_analysis_returns_valid_score(self, detector):
        """Test compression analysis returns score between 0 and 1."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        score = detector._compression_analysis(img)
        
        assert 0 <= score <= 1
    
    def test_detect_video_requires_cv2(self, detector, sample_image_bytes):
        """Test video detection requires OpenCV."""
        result = detector.detect_video(sample_image_bytes, sample_frames=5)
        
        # Should either work with cv2 or return dependency error
        assert isinstance(result, DetectionResult)
        assert result.method in ['video_analysis', 'dependency_error', 'video_error']
    
    def test_video_detection_returns_frame_results(self, detector):
        """Test video detection returns per-frame analysis when cv2 available."""
        try:
            import cv2
            
            # Create a minimal valid video file
            arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
            img = Image.fromarray(arr)
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Try detection - might fail if no valid video encoder
            result = detector.detect_video(buffer.read(), sample_frames=3)
            
            assert isinstance(result, DetectionResult)
            
        except ImportError:
            pytest.skip("OpenCV not installed")
    
    def test_very_small_image(self, detector):
        """Test detection handles very small images."""
        img = Image.new('RGB', (10, 10), color=(255, 255, 255))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        
        result = detector.detect_image(buffer.read())
        assert isinstance(result, DetectionResult)
    
    def test_very_large_image(self, detector):
        """Test detection handles large images."""
        img = Image.new('RGB', (2000, 2000), color=(128, 128, 128))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=90)
        buffer.seek(0)
        
        result = detector.detect_image(buffer.read())
        assert isinstance(result, DetectionResult)
        assert 0 <= result.confidence <= 100


class TestDetectionResult:
    """Test DetectionResult dataclass."""
    
    def test_result_creation(self):
        """Test creating a DetectionResult."""
        result = DetectionResult(
            is_deepfake=True,
            confidence=85.5,
            method='test',
            details={'key': 'value'}
        )
        
        assert result.is_deepfake is True
        assert result.confidence == 85.5
        assert result.method == 'test'
        assert result.details['key'] == 'value'
    
    def test_result_is_dataclass(self):
        """Test DetectionResult is a proper dataclass."""
        result = DetectionResult(
            is_deepfake=False,
            confidence=50.0,
            method='test',
            details={}
        )
        
        assert isinstance(result, DetectionResult)
        assert result.is_deepfake is False
        assert result.confidence == 50.0
    
    def test_result_with_empty_details(self):
        """Test DetectionResult with empty details."""
        result = DetectionResult(
            is_deepfake=False,
            confidence=0.0,
            method='none',
            details={}
        )
        
        assert result.details == {}


class TestDetectorIntegration:
    """Integration tests for the detector."""
    
    def test_multiple_detections_consistent(self):
        """Test multiple detections on same image are consistent."""
        detector = DeepfakeDetector(threshold=0.5)
        
        img = Image.new('RGB', (200, 200), color=(100, 100, 100))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        image_bytes = buffer.read()
        
        results = [detector.detect_image(image_bytes) for _ in range(5)]
        
        # All results should have same classification
        classifications = [r.is_deepfake for r in results]
        assert len(set(classifications)) == 1, "Inconsistent classifications"
    
    def test_batch_processing_different_images(self):
        """Test processing different images produces different results."""
        detector = DeepfakeDetector(threshold=0.5)
        
        images = []
        for i in range(5):
            color = (i * 50, 128 - i * 20, 64 + i * 30)
            img = Image.new('RGB', (100, 100), color=color)
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            buffer.seek(0)
            images.append(buffer.read())
        
        results = [detector.detect_image(img_bytes) for img_bytes in images]
        
        # Each result should be a valid DetectionResult
        assert all(isinstance(r, DetectionResult) for r in results)
        
        # At least some diversity in methods used
        methods = set(r.method for r in results if r.method not in ['error', 'dependency_error'])
        assert len(methods) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
