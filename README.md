# Geospatial Wheels Index for Windows

A [PEP503 compliant index](https://nathanjmcdougall.github.io/geospatial-wheels-index/) for installation of geospatial wheels on Windows, using [Christoph Gohlke](https://github.com/cgohlke)'s wheel builds at <https://github.com/cgohlke/geospatial-wheels>.

## Cross-platform GDAL installation with `uv`

To install `gdal` with both Windows and Linux support, add the following configuration to `pyproject.toml`:

```TOML
[tool.uv.sources]
gdal = [
  { index = "gdal-wheels", marker = "sys_platform == 'linux'" },
  { index = "geospatial_wheels", marker = "sys_platform == 'win32'" },
]

[[tool.uv.index]]
name = "geospatial_wheels"
url = "https://nathanjmcdougall.github.io/geospatial-wheels-index/"
explicit = true

[[tool.uv.index]]
name = "gdal-wheels"
url = "https://gitlab.com/api/v4/projects/61637378/packages/pypi/simple"
explicit = true
```

Then to install, you run:

```bash
uv add gdal
```

Linux support is provided by a [separate project's index](https://gitlab.com/mentaljam/gdal-wheels). See the Acknowledgements section below.

## Simple pip-based installation

You can also use a simple `pip` command to install packages on Windows, e.g. for `gdal` you would run:

```Powershell
pip install gdal --index-url https://nathanjmcdougall.github.io/geospatial-wheels-index/
```

## Other packages: Windows-only installation with `uv`

To install `pygeos` for example, add the following configuration to `pyproject.toml`:

```TOML
[tool.uv.sources]
gdal = [
  { index = "geospatial_wheels", marker = "sys_platform == 'win32'" },
]

[[tool.uv.index]]
name = "geospatial_wheels"
url = "https://nathanjmcdougall.github.io/geospatial-wheels-index/"
explicit = true
```

Then to install, you run:

```bash
uv add pygeos
```

## Acknowledgements

This index is totally dependent on the work of [Christoph Gohlke](https://github.com/cgohlke) to tirelessly build and host wheels for the Python geospatial stack on Windows.

The work of [Petr Tsymbarovich](https://gitlab.com/mentaljam) is also acknowledged for similarly dedicated work at building and hosting wheels for GDAL on Linux, to enable cross-platform installation of `gdal` with `uv`.

Using this index together with indexes for other platforms would not be possible without the work of [Astral](https://astral.sh/), with [uv's powerful index support](https://docs.astral.sh/uv/configuration/indexes/#package-indexes).
