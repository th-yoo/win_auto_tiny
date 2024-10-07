import re
import pytest
from win_auto_tiny.dpi_utils import get_dpi, XYMapper  # Replace with actual import path

def test_get_dpi():
    dpi = get_dpi()
    assert dpi is not None, "DPI should not be None."

def test_xy_mapper_default():
    # Use the singleton instance
    mapper = XYMapper()  # Should use default input DPI (96, 96)
    
    # Get system DPI
    sys_dpi = get_dpi()
    expected_output = (round(100 * sys_dpi[0] / 96), round(100 * sys_dpi[1] / 96))
    
    mapped_coordinates = mapper((100, 100))
    assert mapped_coordinates == expected_output, f"Expected {expected_output}, but got {mapped_coordinates}."

def test_xy_mapper_custom_dpi():
    XYMapper.reset()
    # Use the singleton instance with custom DPI
    custom_dpi = (144, 144)
    mapper = XYMapper(custom_dpi)
    
    # Get system DPI
    sys_dpi = get_dpi()
    expected_output = (round(100 * sys_dpi[0] / custom_dpi[0]), round(100 * sys_dpi[1] / custom_dpi[1]))
    
    mapped_coordinates = mapper((100, 100))
    assert mapped_coordinates == expected_output, f"Expected {expected_output}, but got {mapped_coordinates}."

    # Attempting to create a new instance with a different DPI should raise an error
    with pytest.raises(ValueError, match=re.escape("Cannot instantiate XYMapper with a different input_dpi: (96, 96). Current input_dpi is ") + re.escape(str(custom_dpi)) + "."):
        XYMapper((96, 96))

    # Confirm the existing instance still uses the custom DPI
    assert mapper.input_dpi == custom_dpi, "The input DPI of the existing instance should remain unchanged."

