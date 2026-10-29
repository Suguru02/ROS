"""Tests for expected URDF parent links."""

from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

XACRO_PATH = Path(__file__).resolve().parents[1] / 'urdf' / 'vehicle.urdf.xacro'


def _load_urdf() -> ET.Element:
    """Expand Xacro and parse URDF."""
    urdf_text = subprocess.check_output(
        ['xacro', str(XACRO_PATH)],
        text=True,
    )
    return ET.fromstring(urdf_text)


def test_lidar_parent_is_base_link() -> None:
    """Lidar must be attached directly to base_link."""
    root = _load_urdf()

    joint = next(
        j for j in root.findall('joint')
        if j.get('name') == 'base_to_lidar'
    )

    parent = joint.find('parent')
    child = joint.find('child')
    assert parent is not None
    assert child is not None
    assert parent.get('link') == 'base_link'
    assert child.get('link') == 'lidar_link'
