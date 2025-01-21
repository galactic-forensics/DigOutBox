"""Utilities.

ProxyList is taken from InstrumentKit: https://github.com/Galvant/InstrumentKit
"""

from enum import Enum, IntEnum


class ProxyList:
    """Proxy List class from instrumentkit.

    This is a special class used to generate lists of objects where the valid
    keys are defined by the `valid_set` init parameter. This allows an
    instrument to have a single property through which all of its various
    identical input/ouput channels can be accessed.

    Search the code base of existing examples of how this is used for plenty
    of different examples.

    :param parent: The "parent" or "owner" of the of the proxy classes. In
        dev work, this is typically ``self``.
    :param proxy_cls: The child class that will be returned when the returned
        object is iterated through. These are usually objects that represent
        an entire channel/sensor/input/output, of which an instrument might
        have more than one but each are individually addressed. An example is
        an oscilloscope channel.
    :param valid_set: The set of valid keys by which the proxy class objects
        are accessed. Typically this is something like `range`, but can be
        any generator, list, enum, etc.
    """

    def __init__(self, parent, proxy_cls, valid_set):
        """Initialize the class."""
        self._parent = parent
        self._proxy_cls = proxy_cls
        self._valid_set = valid_set

        # FIXME: This only checks the next level up the chain!
        if hasattr(valid_set, "__bases__"):
            self._isenum = (Enum in valid_set.__bases__) or (
                IntEnum in valid_set.__bases__
            )
        else:
            self._isenum = False

    def __iter__(self):
        """Iterate."""
        for idx in self._valid_set:
            yield self._proxy_cls(self._parent, idx)

    def __getitem__(self, idx):
        """Get an individual item."""
        # If we have an enum, try to normalize by using getitem. This will
        # allow for things like 'x' to be used instead of enum.x.
        if self._isenum:
            try:
                idx = self._valid_set[idx]
            except KeyError:
                try:
                    idx = self._valid_set(idx)
                except ValueError:
                    pass
            if not isinstance(idx, self._valid_set):
                raise IndexError(f"Index out of range. Must be in {self._valid_set}.")
            idx = idx.value
        else:
            if idx not in self._valid_set:
                raise IndexError(f"Index out of range. Must be in {self._valid_set}.")
        return self._proxy_cls(self._parent, idx)

    def __len__(self):
        """Length of the valid set."""
        return len(self._valid_set)
