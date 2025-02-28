def test_importable() -> None:
    import osgeo

    assert osgeo.__version__ is not None
