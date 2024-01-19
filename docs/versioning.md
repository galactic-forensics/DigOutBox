# Versioning

The firmware,
python interface (aka controller_cli),
and GUI (aka controller)
are versioned independently.
The following tags are added
to GitHub:

| Module        | Tag          | Example      |
|---------------|--------------|--------------|
| firmware      | `fw_vXYZ`    | `fw_v020`    |
| controller_cli | `cli_vX.Y.Z` | `cli_0.2.0`  |
| controller   | `gui_vX.Y.Z` | `gui_v0.2.0` |

Here, `X`, `Y`, and `Z`
are follow
[semantic verioning](https://semver.org/)
guidelines and are:

- `X`: Major version (breaking changes)
- `Y`: Minor versions (non-breaking changes)
- `Z`: Patch version (bug fixes)

The dependency flow is as following:

``` mermaid
graph LR
  A[Firmware] --> B[controller_cli];
  B --> C[GUI];
```

This means, e.g.,
that the GUI depends on both,
the firmware and the controller_cli.

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
as well as with controller_cli versions
`cli_v0.1.0` and `cli_v0.2.0`.

!!! warning
    The GUI with version `gui_v0.2.0` however
    will not be compatible with
    firmware or controller_cli versions that are lower than `v0.2.0`.
    The same holds true for the controller_cli,
    which will not be compatible with firmware versions
    with lower minor versions.

## Patch versions

Patch versions are reserved for bug fixes.

## Changelog
