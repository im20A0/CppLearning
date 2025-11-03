# Batch Image Watermark Removal Tool

This is a Python and OpenCV-based batch image watermark removal tool that supports automatic detection and manual specification of watermark locations.

## Features

? **Three Processing Modes**:
- ?? **Auto-detection mode**: Intelligently identifies watermark regions in images
- ?? **Bottom-right mode**: Specifically handles watermarks in the bottom-right corner (most common location)
- ? **Manual mode**: Precisely specify watermark location and size

? **Batch Processing**: Process an entire folder of images at once

? **Multi-format Support**: JPG, PNG, BMP, TIFF, WEBP, etc.

## Installation

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python numpy
```

## Usage

### 1. Auto-detection Mode (Recommended)

Suitable for cases where watermark location is not fixed or watermark color is light:

```bash
python remove_watermark.py -i ./input_images -o ./output_images
```

Adjust detection sensitivity (higher threshold = stricter detection):

```bash
python remove_watermark.py -i ./input_images -o ./output_images -t 220
```

### 2. Bottom-right Mode

Specifically handles watermarks in the bottom-right corner (like "www.magiccardmarket.eu" in your image):

```bash
python remove_watermark.py -i ./input_images -o ./output_images -m bottom-right
```

### 3. Manual Mode

Precisely specify watermark location (requires knowing watermark coordinates and size):

```bash
python remove_watermark.py -i ./input_images -o ./output_images -m manual -r 100 50 200 80
```

Parameter explanation: `-r X Y WIDTH HEIGHT`
- X: X coordinate of watermark top-left corner
- Y: Y coordinate of watermark top-left corner
- WIDTH: Watermark width
- HEIGHT: Watermark height

## Parameters

| Parameter | Short | Description | Required |
|-----------|-------|-------------|----------|
| --input | -i | Input image directory | ? |
| --output | -o | Output image directory | ? |
| --mode | -m | Processing mode (auto/manual/bottom-right) | ? (default: auto) |
| --region | -r | Watermark region (x y width height) | ? (required for manual mode) |
| --threshold | -t | Detection threshold (0-255) | ? (default: 200) |

## Examples

### Example 1: Process All Images in a Folder

```bash
# Create input and output folders
mkdir input_images output_images

# Place images to be processed in the input_images folder

# Run the script (bottom-right mode works best for your case)
python remove_watermark.py -i ./input_images -o ./output_images -m bottom-right
```

### Example 2: Watermark at a Specific Location

If your watermark is always at the same location (e.g., 300x100 region in bottom-right):

```bash
python remove_watermark.py -i ./input_images -o ./output_images -m manual -r 500 380 300 100
```

### Example 3: Adjust Auto-detection Parameters

If auto-detection results are not ideal, adjust the threshold:

```bash
# Higher threshold = stricter (suitable for dark watermarks)
python remove_watermark.py -i ./input_images -o ./output_images -t 180

# Lower threshold = more lenient (suitable for light watermarks)
python remove_watermark.py -i ./input_images -o ./output_images -t 240
```

## How It Works

This tool uses OpenCV's **Image Inpainting** technique:

1. **Detect watermark region**: Determine watermark location through color, brightness, or manual specification
2. **Create mask**: Mark regions that need to be repaired
3. **Intelligent filling**: Use Telea algorithm to analyze surrounding pixels and intelligently fill watermark region

## Notes

?? **Results**:
- Watermark removal effectiveness depends on watermark complexity and background
- Simple text watermarks work best
- Complex patterns or watermarks covering important content may leave traces
- Recommend testing with a few images first, then batch process after adjusting parameters

?? **Copyright Notice**:
- Use only for legal purposes
- Respect original authors' copyrights
- Do not use for infringement

## Advanced Tips

### How to Find Exact Watermark Location?

You can use an image viewer or Python script to check coordinates:

```python
import cv2
img = cv2.imread('your_image.jpg')
print(f"Image dimensions: {img.shape[1]} x {img.shape[0]}")  # width x height
```

For your card images, the "www.magiccardmarket.eu" watermark is usually in the bottom-right corner. Try:
- Bottom-right 60% area: `-m bottom-right`
- Or manually specify (assuming image is 500x700): `-m manual -r 300 620 200 80`

### Batch Process Different Watermark Locations

If watermark locations vary across images:
1. Classify images by watermark location
2. Process each category separately
3. Or use auto-detection mode

## Troubleshooting

**Issue: Watermark not completely removed**
- Solution: Try adjusting threshold `-t` parameter, or use manual mode for precise specification

**Issue: Obvious traces left after removal**
- Solution: Watermark region too large or background too complex, try adjusting region size

**Issue: Non-watermark parts mistakenly removed**
- Solution: Increase threshold `-t` or use manual mode

## Support

For issues or suggestions, please check code comments or adjust parameters for testing.

---

**Happy removing!** ??
