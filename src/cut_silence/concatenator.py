"""
Video concatenator module for joining video segments.
"""

from pathlib import Path
from typing import List


class VideoConcatenator:
    """Concatenates video segments into a single output file."""

    def __init__(self, verbose: bool = False):
        """
        Initialize video concatenator.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose

    def concatenate_segments(
        self, segment_files: List[Path], output_path: Path
    ) -> bool:
        """
        Concatenate video segments into a single file.

        Args:
            segment_files: List of segment file paths to concatenate
            output_path: Path for the output video file

        Returns:
            True if concatenation was successful, False otherwise
        """
        # TODO: Implement using FFmpeg concat demuxer
        # Create concat file list, then:
        # ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
        if self.verbose:
            print(f"Concatenating {len(segment_files)} segments to: {output_path}")

        return False

    def generate_output_path(self, input_path: Path, suffix: str = "_cut") -> Path:
        """
        Generate output file path with auto-rename on collision.

        Args:
            input_path: Input video file path
            suffix: Suffix to add to filename

        Returns:
            Output file path (with collision handling)
        """
        stem = input_path.stem
        ext = input_path.suffix
        parent = input_path.parent

        # Generate base output path
        output_path = parent / f"{stem}{suffix}{ext}"

        # Handle file collision with auto-rename
        counter = 1
        while output_path.exists():
            output_path = parent / f"{stem}{suffix}_{counter}{ext}"
            counter += 1

        return output_path
