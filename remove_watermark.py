#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
??????????
???????????????
"""

import cv2
import numpy as np
import os
import argparse
from pathlib import Path


def detect_watermark_region(image, threshold=200):
    """
    ?????????????????????
    
    Args:
        image: ????
        threshold: ????
    
    Returns:
        mask: ???????
    """
    # ??????
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ??????????????????????
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # ?????????????
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(thresh, kernel, iterations=2)
    
    return mask


def detect_text_watermark(image):
    """
    ??????????????
    
    Args:
        image: ????
    
    Returns:
        mask: ???????
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ??Canny????
    edges = cv2.Canny(gray, 50, 150)
    
    # ?????????
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    return dilated


def remove_watermark_inpaint(image, mask):
    """
    ??OpenCV?inpainting??????
    
    Args:
        image: ????
        mask: ??????
    
    Returns:
        result: ????????
    """
    # ??Telea??????
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    return result


def remove_watermark_manual(image, x, y, width, height):
    """
    ???????????
    
    Args:
        image: ????
        x, y: ???????
        width, height: ???????
    
    Returns:
        result: ????????
    """
    # ????
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[y:y+height, x:x+width] = 255
    
    # ??inpainting??
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    return result


def process_image(input_path, output_path, mode='auto', region=None, threshold=200):
    """
    ??????
    
    Args:
        input_path: ??????
        output_path: ??????
        mode: ???? ('auto', 'manual', 'bottom-right')
        region: ???????? (x, y, width, height)
        threshold: ??????
    """
    # ????
    image = cv2.imread(input_path)
    if image is None:
        print(f"? ??????: {input_path}")
        return False
    
    try:
        if mode == 'manual' and region:
            # ??????
            x, y, width, height = region
            result = remove_watermark_manual(image, x, y, width, height)
        elif mode == 'bottom-right':
            # ?????????????
            h, w = image.shape[:2]
            x, y = int(w * 0.6), int(h * 0.8)
            width, height = w - x, h - y
            result = remove_watermark_manual(image, x, y, width, height)
        else:
            # ??????
            mask = detect_watermark_region(image, threshold)
            result = remove_watermark_inpaint(image, mask)
        
        # ????
        cv2.imwrite(output_path, result)
        print(f"? ????: {output_path}")
        return True
    except Exception as e:
        print(f"? ???? {input_path}: {str(e)}")
        return False


def batch_process(input_dir, output_dir, mode='auto', region=None, threshold=200, extensions=None):
    """
    ??????
    
    Args:
        input_dir: ????
        output_dir: ????
        mode: ????
        region: ????????
        threshold: ??????
        extensions: ???????
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    
    # ??????
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # ????????
    input_path = Path(input_dir)
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"??  ? {input_dir} ?????????")
        return
    
    print(f"?? ?? {len(image_files)} ???")
    print(f"?? ????: {mode}")
    print("-" * 50)
    
    success_count = 0
    for img_file in image_files:
        output_path = Path(output_dir) / img_file.name
        if process_image(str(img_file), str(output_path), mode, region, threshold):
            success_count += 1
    
    print("-" * 50)
    print(f"? ??! ???? {success_count}/{len(image_files)} ???")


def main():
    parser = argparse.ArgumentParser(
        description='??????????',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
????:
  # ?????????
  python remove_watermark.py -i ./input -o ./output

  # ???????
  python remove_watermark.py -i ./input -o ./output -m bottom-right

  # ???????? (x=100, y=50, ??=200, ??=80)
  python remove_watermark.py -i ./input -o ./output -m manual -r 100 50 200 80

  # ??????
  python remove_watermark.py -i ./input -o ./output -t 220
        """
    )
    
    parser.add_argument('-i', '--input', required=True, help='??????')
    parser.add_argument('-o', '--output', required=True, help='??????')
    parser.add_argument('-m', '--mode', choices=['auto', 'manual', 'bottom-right'], 
                        default='auto', help='???? (??: auto)')
    parser.add_argument('-r', '--region', type=int, nargs=4, metavar=('X', 'Y', 'W', 'H'),
                        help='????: ???? (x y width height)')
    parser.add_argument('-t', '--threshold', type=int, default=200,
                        help='?????? (0-255, ??: 200)')
    
    args = parser.parse_args()
    
    # ????
    if args.mode == 'manual' and not args.region:
        parser.error("???????? -r/--region ??")
    
    if not os.path.isdir(args.input):
        parser.error(f"???????: {args.input}")
    
    # ??????
    batch_process(
        input_dir=args.input,
        output_dir=args.output,
        mode=args.mode,
        region=args.region,
        threshold=args.threshold
    )


if __name__ == '__main__':
    main()
