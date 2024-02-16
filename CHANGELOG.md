# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Types of changes

    `Added` for new features.
    `Changed` for changes in existing functionality.
    `Deprecated` for soon-to-be removed features.
    `Removed` for now removed features.
    `Fixed` for any bug fixes.
    `Security` in case of vulnerabilities.
-->

## Unreleased

## v1.9.0

Sync with sila_cetoni v1.9.0 release

### Changed

- All I/O features are now monitored for traffic by `CetoniApplicationSystem`

## v1.8.0

Sync with sila_cetoni v1.8.0 release

### Added

- Support for accessing the I/Os of Kunbus digital and analog I/O modules for the Revolution Pi
- Device driver classes for CETONI I/O channels
- Increase required Python version to 3.8 because in 3.7 the implementation of `ThreadPoolExecutor` in the standard library does not reuse idle threads leading to an ever increasing number of threads which eventually causes blocking of the server(s) on Raspberry Pis

### Changed

- Feature implementations use the more agnostic `IOChannelInterface` to support vendor-independent I/O channels
- Bump required sila2 version to v0.10.1

## v1.7.1

Sync with sila_cetoni v1.7.1 release

### Fixed

- Typo in pyproject.toml

## v1.7.0

Sync with sila_cetoni v1.7.0

### Changed

- Bump required sila2 version to v0.10.0

## v1.6.0

Sync with sila_cetoni v1.6.0

## v1.5.0

Sync with sila_cetoni v1.5.0

## v1.4.0

Sync with sila_cetoni v1.4.0

## v1.3.0

Sync with sila_cetoni v1.3.0

### Fixed

- Properly call `super().stop()` in the feature implementation classes

## v1.2.0

Sync with sila_cetoni v1.2.0

## v1.1.0

### Changed

- Bump sila2 to v0.8.2

## v1.0.0

First release of sila_cetoni

This is the I/O plugin which adds support for controlling CETONI I/O devices via SiLA 2

### Added

- AnalogInChannelProvider feature and feature implementation
- AnalogOutChannelController feature and feature implementation
- DigitalInChannelProvider feature and feature implementation
- DigitalOutChannelController feature and feature implementation
