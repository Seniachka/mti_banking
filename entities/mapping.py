class Mapping:
    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key, default=None):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return default

    def items(self):
        return list(zip(self._keys, self._values))

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)

    def __contains__(self, key):
        return key in self._keys

    def __len__(self):
        return len(self._keys)

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        return self.items() == other.items()

    def __repr__(self):
        return f"Mapping({self.items()!r})"

    def __str__(self):
        return repr(self)