#!/usr/bin/env python3
"""
Setup script for libfreenect Python wrapper
Combines modern setuptools with backward compatibility
"""
import os
import sys
import re
import numpy as np
from setuptools import setup, Extension

def get_cython_version():
    """
    Returns:
        Version as a pair of ints (major, minor)
    Raises:
        ImportError: Can't load cython or find version
    """
    try:
        import Cython.Compiler.Main
        try:
            # New way
            version = Cython.__version__
        except AttributeError:
            # Old way
            version = Cython.Compiler.Main.version
        
        match = re.search(r'^([0-9]+)\.([0-9]+)', version)
        if match:
            return [int(g) for g in match.groups()]
        else:
            raise ImportError("Could not parse Cython version")
    except ImportError:
        raise ImportError("Cython not available")

# Determine source file and build approach
try:
    cython_version = get_cython_version()
    print(f"Found Cython version: {'.'.join(map(str, cython_version))}")
    
    # Handle Cython version compatibility (like your CMake does)
    if cython_version[0] == 0:
        # Use old Cython-compatible file
        source_file = "freenect.cython0.pyx"
        print("Using freenect.cython0.pyx for Cython 0.x")
    else:
        # Use new Cython-compatible file  
        source_file = "freenect.pyx"
        print("Using freenect.pyx for Cython 1.x+")
    
    from Cython.Build import cythonize
    use_cython = True
    
except ImportError:
    print("Cython not found, looking for pre-compiled C files...")
    # Fall back to C files if available
    if os.path.exists("freenect.c"):
        source_file = "freenect.c"
        use_cython = False
        print("Using pre-compiled freenect.c")
    else:
        raise ImportError("Neither Cython nor pre-compiled C files found!")

# Get numpy include directory
numpy_include = np.get_include()

# Base include directories (combining your original paths with new ones)
base_includes = [
    numpy_include,
    "../../include/",  # Your original relative path
    "../c_sync/",      # Your original relative path
]

# Platform-specific library and include paths
if sys.platform == "darwin":  # macOS
    include_dirs = base_includes + [
        "/usr/local/include",
        "/usr/local/include/libfreenect", 
        "/usr/local/include/libusb-1.0",
        "/opt/homebrew/include",
        "/opt/homebrew/include/libfreenect",
        "/opt/homebrew/include/libusb-1.0",
    ]
    library_dirs = [
        "/usr/local/lib",
        "/usr/local/lib64", 
        "/opt/homebrew/lib",
    ]
    libraries = ["usb-1.0", "freenect", "freenect_sync"]
    
elif sys.platform.startswith("linux"):  # Linux
    include_dirs = base_includes + [
        "/usr/include",
        "/usr/include/libfreenect",
        "/usr/include/libusb-1.0/",
        "/usr/local/include",
        "/usr/local/include/libfreenect",
        "/usr/local/include/libusb-1.0",
    ]
    library_dirs = [
        "/usr/lib",
        "/usr/local/lib",
        "/usr/local/lib64",
        "/usr/lib/x86_64-linux-gnu",
    ]
    libraries = ["usb-1.0", "freenect", "freenect_sync"]
    
elif sys.platform == "win32":  # Windows
    include_dirs = base_includes + [
        r"C:\Program Files\libfreenect\include",
        r"C:\libfreenect\include",
    ]
    library_dirs = [
        r"C:\Program Files\libfreenect\lib",
        r"C:\libfreenect\lib",
    ]
    libraries = ["freenect", "freenect_sync"]  # Windows might not need libusb-1.0 explicitly
else:
    # Default fallback
    include_dirs = base_includes
    library_dirs = ["/usr/local/lib", "/usr/local/lib64", "/usr/lib/"]
    libraries = ["usb-1.0", "freenect", "freenect_sync"]

# Define the extension module
extensions = [
    Extension(
        name="freenect",
        sources=[source_file],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        runtime_library_dirs=['/usr/local/lib', '/usr/local/lib64', '/usr/lib/'],
        extra_compile_args=['-fPIC', '-O3'],
        language="c",
    )
]

# Cythonize if using Cython
if use_cython:
    ext_modules = cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
        }
    )
else:
    ext_modules = extensions

if __name__ == "__main__":
    setup(ext_modules=ext_modules)