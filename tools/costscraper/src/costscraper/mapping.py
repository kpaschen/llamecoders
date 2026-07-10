"""Model name normalization between config identifiers and provider names."""


class ModelMapper:
    """Maps raw provider model names to normalized config model identifiers."""

    def __init__(self, providerMappings=None):
        self.providerMappings = providerMappings or {}

    def normalizeName(self, provider, rawName):
        mappings = self.providerMappings.get(provider, {})
        return mappings.get(rawName, rawName)
