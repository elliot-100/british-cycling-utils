# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.6.0] - 2026-09-10

### Added

- `ClubSubscription` data validation; only use 'CSV export' field names in `from_bc_data()`
- Support Python 3.15
- Tests
- CI: add Dependabot

### Changed

- CI: lockfile resolution strategy is now 'lowest-direct'
  i.e. direct dependencies are pinned to the lowest version that satisfies the requirements.

  This should ensure CI flags if dependency lower bounds need to be raised to be
  compatible with a Python version in the CI matrix.


## [0.5.1] - 2026-08-22

### Fixed

- `ClubSubscription.from_bc_data()` could shift dates by one day


## [0.5.0] - 2026-05-05

### Added

- MIT license
- Metadata

### Changed

- Docs: Update `README.md` for PyPI install


## [0.4.0] - 2026-02-23

### Added

- More `ClubSubscription` fields
- Docs: document fields in README

### Changed

- Support Python 3.11

### Fixed

- Type-checking from other projects was broken, due to misplaced `py.typed` marker


## [0.3.1] - 2025-10-08

### Changed

- Require cattrs >= 25.2.0
- CI: support Python 3.14


## [0.3.0] - 2025-09-02

### Changed

- `ClubSubscription.club_membership_expiry` from `datetime.datetime` to `datetime.date`


## [0.2.0] - 2025-08-01

### Added

- README
- build backend
- `py.typed` marker

### Changed

- Rename module and class
- Improved docstrings
- Tests use installed version of project

### Fixed

- mypy was specified as runtime dependency


## [0.1.0] - 2025-07-31

Initial release


[0.6.0]: https://github.com/elliot-100/british-cycling-utils/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/elliot-100/british-cycling-utils/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/elliot-100/british-cycling-utils/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/elliot-100/british-cycling-utils/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/elliot-100/british-cycling-utils/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/elliot-100/british-cycling-utils/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/elliot-100/british-cycling-utils/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/elliot-100/british-cycling-utils/releases/tag/v0.1.0