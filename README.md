# libfreenect Python Wrapper

A Python wrapper for libfreenect, providing access to Microsoft Kinect functionality.

## Installation

### From PyPI (recommended) --Still not added
```bash
pip install freenect
```

### From Source
```bash
git clone https://github.com/yourusername/libfreenect-python.git
cd libfreenect-python
pip install .
```

### For Development
```bash
git clone https://github.com/yourusername/libfreenect-python.git
cd libfreenect-python
pip install -e ".[dev]"
```

## Prerequisites

Before installing, make sure you have libfreenect installed on your system. Follow instructions on official GitHub repository: https://github.com/OpenKinect/libfreenect

## Quick Start

```python
import freenect
import numpy as np

# Get depth image
depth, timestamp = freenect.sync_get_depth()
print(f"Depth image shape: {depth.shape}")

# Get RGB image
rgb, timestamp = freenect.sync_get_video()
print(f"RGB image shape: {rgb.shape}")
```

## Features

- Access to Kinect depth camera
- Access to Kinect RGB camera
- Synchronous and asynchronous APIs
- NumPy array integration
- Cross-platform support (Linux, macOS, Windows)

## Requirements

- Python 3.8+
- NumPy
- libfreenect (system library)

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues

If you encounter any problems, please file an issue along with a detailed description.