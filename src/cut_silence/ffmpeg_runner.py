"""
FFmpeg progress runner module for real-time progress tracking.
"""

import re
import subprocess
from typing import List
from tqdm import tqdm


class FFmpegProgressRunner:
    """
    Executes FFmpeg commands with real-time progress tracking.

    FFmpeg outputs progress information to stderr in this format:
    frame=  123 fps= 45 q=-1.0 size=    1024kB time=00:00:05.00 bitrate=1677.7kbits/s speed=2.5x

    This class parses:
    - time=HH:MM:SS.MS - current position in video
    - speed=Xx - processing speed (for ETA calculation)
    """

    # Regex patterns for parsing FFmpeg progress output
    TIME_PATTERN = re.compile(r'time=(\d+):(\d+):(\d+\.\d+)')
    SPEED_PATTERN = re.compile(r'speed=\s*(\d+\.?\d*)x')

    def __init__(self):
        """Initialize FFmpeg progress runner."""
        pass

    def run_with_progress(
        self,
        cmd: List[str],
        description: str,
        total_duration: float,
        show_progress: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Run FFmpeg command with real-time progress tracking.

        Args:
            cmd: FFmpeg command as list
            description: Description for progress bar
            total_duration: Total expected duration in seconds
            show_progress: Whether to show progress bar

        Returns:
            CompletedProcess object with returncode, stdout, stderr
        """
        if not show_progress or total_duration <= 0:
            # Fall back to simple subprocess.run if no progress needed
            return subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        # Start FFmpeg process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffered
        )

        # Collect stderr output for error reporting
        stderr_lines = []

        # Create progress bar
        with tqdm(
            total=total_duration,
            desc=description,
            unit="s",
            unit_scale=True,
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:.1f}s/{total:.1f}s [{elapsed}<{remaining}, {rate_fmt}]',
            disable=False
        ) as pbar:
            # Read stderr line by line
            if process.stderr:
                for line in process.stderr:
                    stderr_lines.append(line)

                    # Parse progress information
                    current_time = self._parse_time(line)
                    if current_time is not None and current_time <= total_duration:
                        # Update progress bar
                        pbar.n = current_time
                        pbar.refresh()

        # Wait for process to complete
        process.wait()

        # Collect any remaining output
        stdout = process.stdout.read() if process.stdout else ""
        stderr = ''.join(stderr_lines)

        # Create CompletedProcess-like object
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=process.returncode,
            stdout=stdout,
            stderr=stderr
        )

    def _parse_time(self, line: str) -> float:
        """
        Parse time from FFmpeg progress line.

        Args:
            line: FFmpeg stderr line

        Returns:
            Time in seconds, or None if not found
        """
        match = self.TIME_PATTERN.search(line)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3))
            return hours * 3600 + minutes * 60 + seconds
        return None

    def _parse_speed(self, line: str) -> float:
        """
        Parse processing speed from FFmpeg progress line.

        Args:
            line: FFmpeg stderr line

        Returns:
            Speed multiplier (e.g., 2.5 for 2.5x), or None if not found
        """
        match = self.SPEED_PATTERN.search(line)
        if match:
            speed = float(match.group(1))
            # Avoid division by zero and handle edge cases
            return speed if speed > 0 else None
        return None
