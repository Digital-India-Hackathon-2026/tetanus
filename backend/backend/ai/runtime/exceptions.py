class PromptRuntimeError(Exception):
    """Base exception for the Prompt Runtime Engine."""
    pass

class PromptValidationError(PromptRuntimeError):
    """Raised when a prompt template is missing required variables."""
    pass

class ManifestValidationError(PromptRuntimeError):
    """Raised when prompt_manifest.json is malformed or invalid."""
    pass

class CacheError(PromptRuntimeError):
    """Raised for cache retrieval or invalidation failures."""
    pass

class OversizedPromptWarning(Warning):
    """Warning issued when a rendered prompt exceeds soft limits."""
    pass

class MissingDependencyError(PromptRuntimeError):
    """Raised when an AIKB or Schema dependency declared in the manifest is missing."""
    pass
