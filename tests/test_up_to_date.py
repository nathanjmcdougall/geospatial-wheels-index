import os
from pathlib import Path

import httpx
import pytest

PACKAGE_NAMES = [
    "basemap",
    "cartopy",
    "cftime",
    "fiona",
    "gdal",
    "netcdf4",
    "pygeos",
    "pyproj",
    "rasterio",
    "rtree",
    "shapely",
]


def _get_whl_urls() -> list[str]:
    url = "https://api.github.com/repos/cgohlke/geospatial-wheels/releases"
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    releases = response.json()

    whl_urls = []
    for release in releases:
        assert isinstance(release, dict)
        for asset in release.get("assets", []):
            asset_url: str = asset["browser_download_url"]
            if asset_url.endswith(".whl"):
                whl_urls.append(asset_url)

    return whl_urls


def _get_package_name(whl_url: str) -> str:
    return Path(whl_url).name.split("-")[0].lower()


def test_index_up_to_date(tmp_path: Path) -> None:
    """Save asset URLs to a text file, filtering for those containing 'GDAL'."""

    if os.getenv("CI"):  # Don't do this locally due to rate limits
        whl_urls = _get_whl_urls()
        package_names = sorted({_get_package_name(whl_url) for whl_url in whl_urls})
        assert package_names == PACKAGE_NAMES
    else:
        package_names = PACKAGE_NAMES

    html_contents = (
        """\
<!DOCTYPE html>
<html>
  <body>
"""
        + "\n".join(
            [
                f"""    <a href="https://nathanjmcdougall.github.io/geospatial-wheels-windows-flatlinks/{whl_name}/">{whl_name}</a>"""
                for whl_name in package_names
            ]
        )
        + """\
  </body>
</html>
"""
    )

    html_file = tmp_path / "index.html"
    html_file.write_text(html_contents)
    assert (
        html_file.read_text()
        == (Path(__file__).parent.parent / "docs" / "index.html").read_text()
    )


@pytest.mark.skipif(not os.getenv("CI"), reason="API rate limits")
@pytest.mark.parametrize("package_name", PACKAGE_NAMES)
def test_package_versions_up_to_date(package_name: str, tmp_path: Path) -> None:
    """Save asset URLs to a text file, filtering for those containing 'GDAL'."""
    whl_urls = [
        whl_url
        for whl_url in _get_whl_urls()
        if _get_package_name(whl_url) == package_name
    ]

    html_contents = (
        f"""\
<!DOCTYPE html>
<html>
<head><title>{package_name}</title></head>
<body>
    <h1>{package_name}</h1>
"""
        + "\n".join(
            [
                f"""    <a href="{whl_url}">{Path(whl_url).name}</a>"""
                for whl_url in whl_urls
            ]
        )
        + """\
</body>
</html>
"""
    )

    html_file = tmp_path / "index.html"
    html_file.write_text(html_contents)

    pkg_dir = Path(__file__).parent.parent / "docs" / package_name

    if not pkg_dir.exists():
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "index.html").write_text(html_contents)

    assert html_file.read_text() == (pkg_dir / "index.html").read_text()
