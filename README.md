# ArUco Marker Map Generator

This script generates an SVG map with ArUco markers based on a text input file that specifies marker positions and attributes.

## Features
- Reads marker data (ID, size, position) from a `.txt` file.
- Generates high-resolution ArUco markers using OpenCV.
- Optimizes SVG rendering by grouping black pixels into rectangles for better performance.
- Allows customizable scaling and SVG canvas size.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- `svgwrite`
- `numpy`

## Installation
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
