import os, sys

sys.path.insert(0, os.path.join(sys.path[-1], 'CO-DETR'))
print(sys.path)

from .portion_regex import PortionRegex
from .info_ocr import ocr
from .custom_logger import get_logger
from .crop_fabric import FabricCropper