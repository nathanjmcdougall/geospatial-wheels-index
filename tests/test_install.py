import pytest


@pytest.mark.skip(reason="Not ready to pass this test yet.")
def test_importable() -> None:
    import osgeo

    assert osgeo.__version__ is not None
