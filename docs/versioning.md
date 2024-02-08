# Versioning



The firmware,
python interface (aka controller),
and GUI (aka controller_gui)
are versioned independently.
The following tags are added
to GitHub:

| Module          | Tag          | Example      |
|-----------------|--------------|--------------|
| firmware        | `fw_vXYZ`    | `fw_v020`    |
| controller      | `cnt_vX.Y.Z` | `cnt_0.2.0`  |
| controller_gui  | `gui_vX.Y.Z` | `gui_v0.2.0` |

Here, `X`, `Y`, and `Z`
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

!!! note
    The whole project is versioned as well with a GitHub tag,
    e.g., `v0.2`.
    The patch version is omitted in this tag,
    since it is not relevant for the whole project.

## Major versions

Major versions are reserved for breaking changes.
This means that either the hardware,
firmware,
or the software are incompatible with previous versions.

## Minor versions

Minor versions are reserved for non-breaking changes,
where new features are added.
A GUI version `gui_0.1.0` will be compatible
with firmware versions `fw_v010` and `fw_v020`
as well as with controllerversions
`cnt_v0.1.0` and `cnt_v0.2.0`.

!!! warning
    The GUI with version `gui_v0.2.0` however
    will not be compatible with
    firmware or controller versions that are lower than `v0.2.0`.
    The same holds true for the controller,
    which will not be compatible with firmware versions
    with lower minor versions.

## Patch versions

Patch versions are reserved for bug fixes.

## Changelog

See [here](changelog.md).
