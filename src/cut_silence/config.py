"""
Configuration constants and defaults for Cut-Silence.
"""

# Default silence detection parameters
DEFAULT_SILENCE_THRESHOLD = -30  # dB
DEFAULT_MIN_SILENCE_DURATION = 0.5  # seconds
DEFAULT_PADDING = 0.0  # seconds

# Output file naming
OUTPUT_SUFFIX = "_cut"

# Supported video formats
SUPPORTED_FORMATS = [".mp4"]

# FFmpeg parameters
FFMPEG_LOGLEVEL = "error"  # Only show errors by default
