# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres mostly to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). However, all releases before 1.0.0 have breaking changes between minor-version updates.

## [1.4.0] - Unreleased

### Changed

- Moved version information to `__version__` attribute in top-level `__init__.py` to comply with Python conventions.
- Floating point numbers no longer use scientific notation, but must use the `[##.###]` syntax

### Added

- `[]` characters to signal to the parse that all value between the braces should be treated as a single literal value
- `DBQuery` to the default imports in the top-level `__init__.py`

### Fixed

- Parsing error with floating point values

## [1.3.1] - 2024-03-25

### Added

- Add `py.typed` and `MANIFEST.in` files to prevent typing warnings

## [1.3.0] - 2024-03-12

_initial Python release._

[1.3.0]: https://github.com/ShiJbey/RePraxisPy/releases/tag/v1.3.0
[1.3.1]: https://github.com/ShiJbey/RePraxisPy/releases/tag/v1.3.1
[1.4.0]: https://github.com/ShiJbey/RePraxisPy/releases/tag/v1.4.0
