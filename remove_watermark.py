#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Watermark Removal Tool
Supports automatic detection and manual watermark region specification
"""

import cv2
import numpy as np
import os
import argparse
from pathlib import Path


def detect_watermark_region(image, threshold=200):
    """
    Automatically detect watermark region in image (based on brightness and color)
    
    Args:
        image: Input image
        threshold: Detection threshold
    
    Returns:
        mask: Mask of watermark region
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect bright regions (watermarks are usually semi-transparent white or light colored)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Morphological operations to connect nearby regions
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(thresh, kernel, iterations=2)
    
    return mask


def detect_text_watermark(image):
    """
    Detect text watermark (based on edge detection)
    
    Args:
        image: Input image
    
    Returns:
        mask: Mask of watermark region
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Dilate to connect text characters
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    return dilated


def remove_watermark_inpaint(image, mask):
    """
    Remove watermark using OpenCV's inpainting algorithm
    
    Args:
        image: Original image
        mask: Watermark region mask
    
    Returns:
        result: Image with watermark removed
    """
    # Use Telea algorithm for inpainting
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    return result


def remove_watermark_manual(image, x, y, width, height):
    """
    Manually specify watermark location and remove it
    
    Args:
        image: Original image
        x, y: Top-left coordinates of watermark
        width, height: Width and height of watermark
    
    Returns:
        result: Image with watermark removed
    """
    # Create mask
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[y:y+height, x:x+width] = 255
    
    # Remove using inpainting
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    return result


def process_image(input_path, output_path, mode='auto', region=None, threshold=200):
    """
    Process a single image
    
    Args:
        input_path: Input image path
        output_path: Output image path
        mode: Processing mode ('auto', 'manual', 'bottom-right')
        region: Region in manual mode (x, y, width, height)
        threshold: Auto-detection threshold
    """
    # Read image
    image = cv2.imread(input_path)
    if image is None:
        print(f"? Unable to read image: {input_path}")
        return False
    
    try:
        if mode == 'manual' and region:
            # Manually specified region
            x, y, width, height = region
            result = remove_watermark_manual(image, x, y, width, height)
        elif mode == 'bottom-right':
            # Process bottom-right watermark (common location)
            h, w = image.shape[:2]
            x, y = int(w * 0.6), int(h * 0.8)
            width, height = w - x, h - y
            result = remove_watermark_manual(image, x, y, width, height)
        else:
            # Auto-detection mode
            mask = detect_watermark_region(image, threshold)
            result = remove_watermark_inpaint(image, mask)
        
        # Save result
        cv2.imwrite(output_path, result)
        print(f"? Processing complete: {output_path}")
        return True
    except Exception as e:
        print(f"? Processing failed {input_path}: {str(e)}")
        return False


def batch_process(input_dir, output_dir, mode='auto', region=None, threshold=200, extensions=None):
    """
    Batch process images
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
        mode: Processing mode
        region: Region in manual mode
        threshold: Auto-detection threshold
        extensions: Supported image formats
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    input_path = Path(input_dir)
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"??  No image files found in {input_dir}")
        return
    
    print(f"?? Found {len(image_files)} images")
    print(f"?? Processing mode: {mode}")
    print("-" * 50)
    
    success_count = 0
    for img_file in image_files:
        output_path = Path(output_dir) / img_file.name
        if process_image(str(img_file), str(output_path), mode, region, threshold):
            success_count += 1
    
    print("-" * 50)
    print(f"? Complete! Successfully processed {success_count}/{len(image_files)} images")


def main():
    parser = argparse.ArgumentParser(
        description='Batch Watermark Removal Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  # Auto-detect and remove watermarks
  python remove_watermark.py -i ./input -o ./output

  # Process bottom-right watermark
  python remove_watermark.py -i ./input -o ./output -m bottom-right

  # Manually specify watermark location (x=100, y=50, width=200, height=80)
  python remove_watermark.py -i ./input -o ./output -m manual -r 100 50 200 80

  # Adjust detection threshold
  python remove_watermark.py -i ./input -o ./output -t 220
        """
    )
    
    parser.add_argument('-i', '--input', required=True, help='Input image directory')
    parser.add_argument('-o', '--output', required=True, help='Output image directory')
    parser.add_argument('-m', '--mode', choices=['auto', 'manual', 'bottom-right'], 
                        default='auto', help='Processing mode (default: auto)')
    parser.add_argument('-r', '--region', type=int, nargs=4, metavar=('X', 'Y', 'W', 'H'),
                        help='Manual mode: watermark region (x y width height)')
    parser.add_argument('-t', '--threshold', type=int, default=200,
                        help='Auto-detection threshold (0-255, default: 200)')
    
    args = parser.parse_args()
    
    # Validate parameters
    if args.mode == 'manual' and not args.region:
        parser.error("Manual mode requires -r/--region parameter")
    
    if not os.path.isdir(args.input):
        parser.error(f"Input directory does not exist: {args.input}")
    
    # Execute batch processing
    batch_process(
        input_dir=args.input,
        output_dir=args.output,
        mode=args.mode,
        region=args.region,
        threshold=args.threshold
    )


if __name__ == '__main__':
    main()
