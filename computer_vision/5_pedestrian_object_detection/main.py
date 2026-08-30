#!/usr/bin/env python3
"""Detect pedestrians in an image or video with OpenCV's built-in HOG detector."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".pgm", ".png", ".ppm", ".tif", ".tiff", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect pedestrians with HOG + a pretrained linear SVM.")
    parser.add_argument("--input", required=True, type=Path, help="Input image or video")
    parser.add_argument("--output", required=True, type=Path, help="Annotated image or video")
    parser.add_argument(
        "--hit-threshold", type=float, default=0.5,
        help="SVM decision threshold; lower values find more candidates and false positives",
    )
    parser.add_argument("--scale", type=float, default=1.03, help="Image-pyramid scale factor (>1)")
    parser.add_argument("--group-threshold", type=int, default=1, help="Rectangle grouping threshold (>=0)")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not args.input.is_file():
        raise ValueError(f"input file does not exist: {args.input}")
    if args.scale <= 1.0:
        raise ValueError("--scale must be greater than 1")
    if args.group_threshold < 0:
        raise ValueError("--group-threshold must be zero or greater")
    args.output.parent.mkdir(parents=True, exist_ok=True)


def make_detector() -> cv2.HOGDescriptor:
    detector = cv2.HOGDescriptor()
    detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    return detector


def detect(
    detector: cv2.HOGDescriptor, frame: np.ndarray, args: argparse.Namespace
) -> list[tuple[int, int, int, int, float]]:
    boxes, weights = detector.detectMultiScale(
        frame,
        hitThreshold=args.hit_threshold,
        winStride=(8, 8),
        padding=(8, 8),
        scale=args.scale,
        groupThreshold=args.group_threshold,
    )
    detections = []
    for (x, y, width, height), weight in zip(boxes, weights):
        detections.append((int(x), int(y), int(width), int(height), float(weight)))
    return detections


def annotate(frame: np.ndarray, detections: list[tuple[int, int, int, int, float]]) -> np.ndarray:
    result = frame.copy()
    for x, y, width, height, confidence in detections:
        cv2.rectangle(result, (x, y), (x + width, y + height), (20, 215, 95), 3)
        label_y = max(24, y - 8)
        cv2.putText(
            result, f"person {confidence:.2f}", (x, label_y), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (20, 215, 95), 2, cv2.LINE_AA,
        )
    return result


def process_image(detector: cv2.HOGDescriptor, args: argparse.Namespace) -> int:
    image = cv2.imread(str(args.input), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"OpenCV could not decode image: {args.input}")
    detections = detect(detector, image, args)
    if not cv2.imwrite(str(args.output), annotate(image, detections)):
        raise ValueError(f"could not write output image: {args.output}")
    print(f"Detections: {len(detections)}")
    print(f"Annotated image: {args.output}")
    return len(detections)


def process_video(detector: cv2.HOGDescriptor, args: argparse.Namespace) -> int:
    capture = cv2.VideoCapture(str(args.input))
    if not capture.isOpened():
        raise ValueError(f"OpenCV could not open video: {args.input}")
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    if width <= 0 or height <= 0:
        capture.release()
        raise ValueError("video contains no readable frame dimensions")
    writer = cv2.VideoWriter(
        str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    if not writer.isOpened():
        capture.release()
        raise ValueError(f"could not create output video: {args.output}")

    frame_count = 0
    detection_count = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        detections = detect(detector, frame, args)
        detection_count += len(detections)
        writer.write(annotate(frame, detections))
        frame_count += 1
    capture.release()
    writer.release()
    if frame_count == 0:
        args.output.unlink(missing_ok=True)
        raise ValueError("video contains no readable frames")
    print(f"Frames: {frame_count}")
    print(f"Total frame detections: {detection_count}")
    print(f"Annotated video: {args.output}")
    return detection_count


def run(args: argparse.Namespace) -> int:
    validate_args(args)
    detector = make_detector()
    if args.input.suffix.lower() in IMAGE_SUFFIXES:
        return process_image(detector, args)
    return process_video(detector, args)


def main() -> int:
    try:
        run(parse_args())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
