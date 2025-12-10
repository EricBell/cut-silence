"""
Progress reporter module for displaying processing progress.
"""

from typing import Optional
from tqdm import tqdm


class ProgressReporter:
    """Reports processing progress to the user."""

    def __init__(self, verbose: bool = False):
        """
        Initialize progress reporter.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.current_bar: Optional[tqdm] = None

    def start_progress(self, description: str, total: int) -> None:
        """
        Start a new progress bar.

        Args:
            description: Description of the task
            total: Total number of items to process
        """
        if self.current_bar:
            self.current_bar.close()

        self.current_bar = tqdm(
            total=total,
            desc=description,
            unit="item",
            disable=not self.verbose,
        )

    def update_progress(self, amount: int = 1) -> None:
        """
        Update progress bar.

        Args:
            amount: Amount to increment the progress bar
        """
        if self.current_bar:
            self.current_bar.update(amount)

    def finish_progress(self) -> None:
        """Close the current progress bar."""
        if self.current_bar:
            self.current_bar.close()
            self.current_bar = None

    def print_summary(
        self,
        input_duration: float,
        output_duration: float,
        segments_removed: int,
    ) -> None:
        """
        Print processing summary.

        Args:
            input_duration: Original video duration in seconds
            output_duration: Output video duration in seconds
            segments_removed: Number of silent segments removed
        """
        time_saved = input_duration - output_duration
        reduction_percent = (time_saved / input_duration * 100) if input_duration > 0 else 0

        print(f"\nProcessing Summary:")
        print(f"  Original duration: {self._format_time(input_duration)}")
        print(f"  Output duration:   {self._format_time(output_duration)}")
        print(f"  Time saved:        {self._format_time(time_saved)} ({reduction_percent:.1f}%)")
        print(f"  Segments removed:  {segments_removed}")

    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Format seconds as HH:MM:SS.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
