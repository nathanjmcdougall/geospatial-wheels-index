from pathlib import Path

import httpx


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


def test_up_to_date(tmp_path: Path) -> None:
    """Save asset URLs to a text file, filtering for those containing 'GDAL'."""
    whl_urls = _get_whl_urls()

    html_contents = (
        """\
<!DOCTYPE html>
<html>

<head>
    <title>geospatial-wheels-windows-flatlinks</title>
</head>

<body>
    <h1>geospatial-wheels-windows-flatlinks</h1>
    <pre>
"""
        + "\n".join(
            [
                f"""<a href="{whl_url}" download="{Path(whl_url).name}">{Path(whl_url).name}</a>"""
                for whl_url in whl_urls
            ]
        )
        + """\
</pre>
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
