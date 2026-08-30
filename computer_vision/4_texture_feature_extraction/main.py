#!/usr/bin/env python3
"""Extract GLCM texture features from an image and compare image patches."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import graycomatrix, graycoprops


FEATURES = ("contrast", "dissimilarity", "homogeneity", "energy", "correlation")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract GLCM texture features from an image and its quadrants."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input image path")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("texture_output"), help="Output directory"
    )
    parser.add_argument("--levels", type=int, default=16, help="Gray levels after quantization (2-256)")
    parser.add_argument("--distance", type=int, default=1, help="Positive pixel-pair distance")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not args.input.is_file():
        raise ValueError(f"input file does not exist: {args.input}")
    if not 2 <= args.levels <= 256:
        raise ValueError("--levels must be between 2 and 256")
    if args.distance < 1:
        raise ValueError("--distance must be at least 1")


def quantize(gray: np.ndarray, levels: int) -> np.ndarray:
    return np.floor(gray.astype(np.float32) * levels / 256).clip(0, levels - 1).astype(np.uint8)


def glcm_features(gray: np.ndarray, levels: int, distance: int) -> dict[str, float]:
    matrix = graycomatrix(
        quantize(gray, levels),
        distances=[distance],
        angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4],
        levels=levels,
        symmetric=True,
        normed=True,
    )
    return {name: float(graycoprops(matrix, name).mean()) for name in FEATURES}


def extract_patches(gray: np.ndarray) -> list[tuple[str, np.ndarray]]:
    height, width = gray.shape
    if height < 4 or width < 4:
        raise ValueError("input image must be at least 4x4 pixels")
    mid_y, mid_x = height // 2, width // 2
    return [
        ("top_left", gray[:mid_y, :mid_x]),
        ("top_right", gray[:mid_y, mid_x:]),
        ("bottom_left", gray[mid_y:, :mid_x]),
        ("bottom_right", gray[mid_y:, mid_x:]),
    ]


def write_csv(path: Path, rows: list[tuple[str, dict[str, float]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["region", *FEATURES])
        writer.writeheader()
        for region, features in rows:
            writer.writerow({"region": region, **{key: f"{value:.6f}" for key, value in features.items()}})


def write_comparison(
    path: Path, patches: list[tuple[str, np.ndarray]], rows: list[tuple[str, dict[str, float]]]
) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(8, 7), constrained_layout=True)
    for axis, (name, patch), (_, features) in zip(axes.flat, patches, rows):
        axis.imshow(patch, cmap="gray", vmin=0, vmax=255)
        axis.set_title(f"{name.replace('_', ' ').title()}\ncontrast={features['contrast']:.2f}")
        axis.axis("off")
    figure.suptitle("Texture patch comparison (GLCM)", fontsize=15)
    figure.savefig(path, dpi=150)
    plt.close(figure)


def run(args: argparse.Namespace) -> tuple[Path, Path]:
    validate_args(args)
    gray = cv2.imread(str(args.input), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise ValueError(f"OpenCV could not decode input image: {args.input}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    patches = extract_patches(gray)
    regions = [("whole_image", gray), *patches]
    rows = [(name, glcm_features(region, args.levels, args.distance)) for name, region in regions]
    csv_path = args.output_dir / "texture_features.csv"
    image_path = args.output_dir / "patch_comparison.png"
    write_csv(csv_path, rows)
    write_comparison(image_path, patches, rows[1:])
    return csv_path, image_path


def main() -> int:
    try:
        csv_path, image_path = run(parse_args())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"Features: {csv_path}")
    print(f"Comparison: {image_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
