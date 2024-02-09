# Versioning



The firmware,
python interface (aka controller),
and GUI (aka controller_gui)
are versioned independently.
Each one gets a version number as following:

- Firmware: `vXYZ`
- Controller: `vX.Y.Z`
- GUI: `vX.Y.Z`

The overall project is also versioned and tagged on GitHub.
Each tag is named `vX.Y.Z` and is associated with a release.

In above examples, `X`, `Y`, and `Z`
follow
[semantic versioning](https://semver.org/)
guidelines and are:

- `X`: Major version (breaking changes)
- `Y`: Minor version (non-breaking changes)
- `Z`: Patch version (bug fixes)

The dependency flow is as following:

``` mermaid
graph LR
  A[Firmware] --> B[controller];
  B --> C[GUI];
```

This means, e.g.,
that the GUI depends on both,
the firmware and the controller.

Generally, major and minor versions for every part of the project should agree with each other.
The patch version can and will differ.

!!! note
    The patch version for the whole project
    is the sum of all the firmware, controller, and GUI patch versions.

## Major versions

Major versions are reserved for breaking changes.
This means that either the hardware,
firmware,
or the software are incompatible with previous versions.

## Minor versions

Minor versions are reserved for non-breaking changes,
where new features are added.
A GUI version `v0.1.0` will be compatible
with firmware versions `v010` and `v020`
as well as with controller versions
`v0.1.0` and `v0.2.0`.

!!! warning
    The GUI with version `v0.2.0` however
    will not be compatible with
    firmware or controller versions that are lower than `v0.2.0`.
    The same holds true for the controller,
    which will not be compatible with firmware versions
    with lower minor versions.

## Patch versions

Patch versions are reserved for bug fixes.

## Changelog

See [here](changelog.md).
