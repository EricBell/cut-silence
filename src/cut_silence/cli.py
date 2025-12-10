"""
CLI parser and main entry point for Cut-Silence.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from cut_silence.config import (
    DEFAULT_SILENCE_THRESHOLD,
    DEFAULT_MIN_SILENCE_DURATION,
    DEFAULT_PADDING,
)


def parse_arguments(args: List[str] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="cut-silence",
        description="Automatically remove silence from MP4 videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cut-silence video.mp4                    # Process single video
  cut-silence *.mp4                        # Process multiple videos
  cut-silence video.mp4 --threshold -35    # Custom silence threshold
  cut-silence video.mp4 --padding 0.3      # Add padding around speech
  cut-silence video.mp4 --dry-run          # Preview without processing
        """,
    )

    parser.add_argument(
        "input_files",
        nargs="+",
        type=Path,
        help="Input video file(s) to process",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path (only valid for single input file)",
    )

    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=DEFAULT_SILENCE_THRESHOLD,
        help=f"Silence threshold in dB (default: {DEFAULT_SILENCE_THRESHOLD})",
    )

    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=DEFAULT_MIN_SILENCE_DURATION,
        help=f"Minimum silence duration in seconds (default: {DEFAULT_MIN_SILENCE_DURATION})",
    )

    parser.add_argument(
        "-p",
        "--padding",
        type=float,
        default=DEFAULT_PADDING,
        help=f"Padding around speech in seconds (default: {DEFAULT_PADDING})",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without processing",
    )

    parser.add_argument(
        "--export-segments",
        type=Path,
        help="Export segment timestamps to JSON file",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    return parser.parse_args(args)


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate parsed arguments."""
    # Check if output is specified with multiple input files
    if args.output and len(args.input_files) > 1:
        print("Error: --output can only be used with a single input file", file=sys.stderr)
        sys.exit(1)

    # Check if all input files exist
    for input_file in args.input_files:
        if not input_file.exists():
            print(f"Error: Input file not found: {input_file}", file=sys.stderr)
            sys.exit(1)

        if not input_file.is_file():
            print(f"Error: Not a file: {input_file}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point for Cut-Silence CLI."""
    args = parse_arguments()
    validate_arguments(args)

    if args.verbose:
        print(f"Cut-Silence v0.1.0")
        print(f"Processing {len(args.input_files)} file(s)...")
        print(f"Silence threshold: {args.threshold} dB")
        print(f"Min silence duration: {args.duration}s")
        print(f"Padding: {args.padding}s")
        print(f"Dry-run: {args.dry_run}")
        print()

    # TODO: Implement video processing pipeline
    # 1. Analyze video for silence
    # 2. Process segments
    # 3. Concatenate non-silent segments
    # 4. Save output

    for input_file in args.input_files:
        print(f"Processing: {input_file}")
        # TODO: Call processing pipeline

    print("Done!")


if __name__ == "__main__":
    main()
