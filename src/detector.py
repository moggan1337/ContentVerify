"""
Deepfake Detection Module

Provides image and video analysis for detecting AI-generated or manipulated content.
Uses pixel-level analysis, statistical patterns, and frequency domain analysis.
"""

import io
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image


@dataclass
class DetectionResult:
    """Result of a deepfake detection analysis."""
    is_deepfake: bool
    confidence: float
    method: str
    details: dict


class DeepfakeDetector:
    """
    Deepfake detection using multiple analysis techniques.
    
    Techniques used:
    - ELA (Error Level Analysis)
    - Frequency domain analysis (DCT)
    - Color histogram analysis
    - Noise pattern detection
    - Compression artifact analysis
    """
    
    def __init__(self, threshold: float = 0.5):
        """
        Initialize the detector.
        
        Args:
            threshold: Confidence threshold for deepfake classification (0-1)
        """
        self.threshold = threshold
        
    def detect_image(self, image_data: bytes) -> DetectionResult:
        """
        Analyze an image for signs of manipulation or AI generation.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            DetectionResult with classification and confidence score
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            results = []
            
            # Run multiple detection techniques
            ela_score = self._ela_analysis(img)
            results.append(('ela', ela_score))
            
            freq_score = self._frequency_analysis(img)
            results.append(('frequency', freq_score))
            
            noise_score = self._noise_analysis(img)
            results.append(('noise', noise_score))
            
            histogram_score = self._histogram_analysis(img)
            results.append(('histogram', histogram_score))
            
            compression_score = self._compression_analysis(img)
            results.append(('compression', compression_score))
            
            # Weighted ensemble of all techniques
            weights = {'ela': 0.25, 'frequency': 0.25, 'noise': 0.2, 'histogram': 0.15, 'compression': 0.15}
            
            final_score = sum(score * weights[name] for name, score in results)
            
            # Determine if deepfake based on threshold
            is_deepfake = final_score > self.threshold
            
            # Get the technique with highest anomaly score for explanation
            primary_method = max(results, key=lambda x: x[1])
            
            return DetectionResult(
                is_deepfake=is_deepfake,
                confidence=min(final_score * 100, 100.0),
                method=primary_method[0],
                details={
                    'ela_score': ela_score,
                    'frequency_score': freq_score,
                    'noise_score': noise_score,
                    'histogram_score': histogram_score,
                    'compression_score': compression_score,
                    'image_size': img.size,
                    'image_mode': img.mode
                }
            )
            
        except Exception as e:
            return DetectionResult(
                is_deepfake=False,
                confidence=0.0,
                method='error',
                details={'error': str(e)}
            )
    
    def detect_video(self, video_data: bytes, sample_frames: int = 10) -> DetectionResult:
        """
        Analyze a video for signs of deepfake manipulation.
        
        Args:
            video_data: Raw video bytes
            sample_frames: Number of frames to sample for analysis
            
        Returns:
            DetectionResult with classification and confidence score
        """
        try:
            import cv2
            
            # Save video data to temporary file for OpenCV
            nparr = np.frombuffer(video_data, np.uint8)
            cap = cv2.VideoCapture(io.BytesIO(nparr.tobytes()))
            
            if not cap.isOpened():
                return DetectionResult(
                    is_deepfake=False,
                    confidence=0.0,
                    method='video_error',
                    details={'error': 'Could not open video'}
                )
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if total_frames == 0:
                return DetectionResult(
                    is_deepfake=False,
                    confidence=0.0,
                    method='video_error',
                    details={'error': 'No frames found in video'}
                )
            
            # Sample frames evenly throughout the video
            frame_indices = np.linspace(0, total_frames - 1, min(sample_frames, total_frames), dtype=int)
            
            frame_scores = []
            frame_results = []
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                
                if ret:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Analyze this frame
                    ela_score = self._ela_analysis(pil_image)
                    freq_score = self._frequency_analysis(pil_image)
                    noise_score = self._noise_analysis(pil_image)
                    
                    frame_score = (ela_score + freq_score + noise_score) / 3
                    frame_scores.append(frame_score)
                    frame_results.append({
                        'frame': int(idx),
                        'ela': ela_score,
                        'frequency': freq_score,
                        'noise': noise_score,
                        'score': frame_score
                    })
            
            cap.release()
            
            if not frame_scores:
                return DetectionResult(
                    is_deepfake=False,
                    confidence=0.0,
                    method='video_error',
                    details={'error': 'Could not extract frames'}
                )
            
            # Calculate overall video score
            avg_score = np.mean(frame_scores)
            std_score = np.std(frame_scores)
            
            # High variance between frames might indicate manipulation
            variance_penalty = min(std_score * 2, 0.2)
            
            final_score = min(avg_score + variance_penalty, 1.0)
            
            is_deepfake = final_score > self.threshold
            
            return DetectionResult(
                is_deepfake=is_deepfake,
                confidence=min(final_score * 100, 100.0),
                method='video_analysis',
                details={
                    'total_frames': total_frames,
                    'fps': fps,
                    'frames_analyzed': len(frame_scores),
                    'frame_scores': frame_results,
                    'variance': float(std_score),
                    'video_score': float(final_score)
                }
            )
            
        except ImportError:
            return DetectionResult(
                is_deepfake=False,
                confidence=0.0,
                method='dependency_error',
                details={'error': 'OpenCV (cv2) required for video analysis'}
            )
        except Exception as e:
            return DetectionResult(
                is_deepfake=False,
                confidence=0.0,
                method='video_error',
                details={'error': str(e)}
            )
    
    def _ela_analysis(self, img: Image.Image) -> float:
        """
        Error Level Analysis - detects inconsistencies in compression artifacts.
        
        Higher scores indicate more inconsistency, possibly from manipulation.
        """
        # Save and re-load at different quality levels
        buffer1 = io.BytesIO()
        img.save(buffer1, format='JPEG', quality=95)
        buffer1.seek(0)
        compressed = Image.open(buffer1)
        
        # Convert to arrays
        arr1 = np.array(img.convert('RGB')).astype(np.float32)
        arr2 = np.array(compressed.convert('RGB')).astype(np.float32)
        
        # Calculate difference
        diff = np.abs(arr1 - arr2)
        
        # Calculate ELA score based on variance of differences
        ela_variance = np.var(diff)
        max_diff = np.max(diff)
        
        # Normalize score
        score = (ela_variance / 1000 + max_diff / 50) / 2
        return min(score, 1.0)
    
    def _frequency_analysis(self, img: Image.Image) -> float:
        """
        DCT-based frequency analysis - detects unnatural high-frequency patterns.
        
        GAN-generated images often have distinctive frequency signatures.
        """
        arr = np.array(img.convert('RGB')).astype(np.float32)
        
        # Apply DCT to each channel
        scores = []
        for channel in range(3):
            channel_data = arr[:, :, channel]
            
            # Simple 2D DCT approximation using numpy FFT
            dct = np.fft.fft2(channel_data)
            dct_shifted = np.fft.fftshift(dct)
            
            # Analyze frequency distribution
            magnitude = np.abs(dct_shifted)
            
            # High-frequency ratio
            h, w = magnitude.shape
            center_h, center_w = h // 2, w // 2
            
            # Extract high and low frequency components
            low_freq = magnitude[center_h-10:center_h+10, center_w-10:center_w+10].mean()
            high_freq_total = magnitude.sum() - magnitude[center_h-50:center_h+50, center_w-50:center_w+50].sum()
            
            # Abnormal high-frequency content might indicate AI generation
            freq_ratio = high_freq_total / (low_freq + 1e-10)
            scores.append(min(freq_ratio / 1000, 1.0))
        
        return np.mean(scores)
    
    def _noise_analysis(self, img: Image.Image) -> float:
        """
        Noise pattern analysis - detects inconsistent noise levels.
        
        Natural images have consistent noise patterns; manipulated images often don't.
        """
        arr = np.array(img.convert('RGB')).astype(np.float32)
        
        # Apply denoising filter to estimate noise
        from scipy.ndimage import uniform_filter
        
        # Local mean
        local_mean = uniform_filter(arr, size=5)
        # Local variance (noise estimate)
        local_var = uniform_filter((arr - local_mean) ** 2, size=5)
        
        # Calculate noise statistics
        noise_std = np.sqrt(np.mean(local_var))
        
        # Normalize - very low or very high noise might be suspicious
        if noise_std < 1:
            return 0.3  # Suspiciously clean
        elif noise_std > 50:
            return 0.7  # Unusually noisy
        else:
            # Check for noise inconsistencies across the image
            noise_map = np.sqrt(local_var)
            noise_variance = np.var(noise_map)
            
            # High variance in noise might indicate manipulation
            return min(noise_variance / 100, 1.0)
    
    def _histogram_analysis(self, img: Image.Image) -> float:
        """
        Color histogram analysis - detects unnatural color distributions.
        
        GAN-generated images often have distinctive color histogram patterns.
        """
        arr = np.array(img.convert('RGB'))
        
        scores = []
        for channel in range(3):
            hist, _ = np.histogram(arr[:, :, channel], bins=256, range=(0, 256))
            hist = hist / hist.sum()  # Normalize
            
            # Check for unusual histogram characteristics
            # 1. Entropy (unusual entropy might indicate generation)
            entropy = -np.sum(hist * np.log2(hist + 1e-10))
            
            # Natural images typically have entropy around 7-8 for each channel
            entropy_deviation = abs(entropy - 7.5)
            
            # 2. Check for unusual peaks or gaps
            peaks = np.where(hist > 0.01)[0]
            if len(peaks) > 0:
                gaps = np.diff(peaks)
                unusual_gaps = np.sum(gaps > 20)
                peak_score = min(unusual_gaps / 10, 1.0)
            else:
                peak_score = 0.5
            
            channel_score = (entropy_deviation / 10 + peak_score) / 2
            scores.append(min(channel_score, 1.0))
        
        return min(np.mean(scores), 1.0)
    
    def _compression_analysis(self, img: Image.Image) -> float:
        """
        Compression artifact analysis - detects inconsistent compression patterns.
        
        Authentic images typically show consistent compression artifacts.
        """
        # Save at multiple quality levels
        scores = []
        
        for quality in [95, 75, 50]:
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            buffer.seek(0)
            recompressed = Image.open(buffer)
            
            arr1 = np.array(img.convert('RGB')).astype(np.float32)
            arr2 = np.array(recompressed.convert('RGB')).astype(np.float32)
            
            # Calculate compression artifacts
            mse = np.mean((arr1 - arr2) ** 2)
            
            # Very low MSE at low quality might indicate synthetic origin
            if quality == 50:
                if mse < 100:
                    scores.append(0.6)  # Suspiciously similar
                else:
                    scores.append(0.3)
            else:
                scores.append(min(mse / 500, 0.5))
        
        return np.mean(scores)
