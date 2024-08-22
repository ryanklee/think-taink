class ThinkTankException(Exception):
    """Base exception class for Think Tank Simulation"""
    pass

class InputProcessingError(ThinkTankException):
    """Raised when there's an error processing input"""
    pass

class LLMPoolError(ThinkTankException):
    """Raised when there's an error with the LLM pool"""
    pass

class ModerationError(ThinkTankException):
    """Raised when there's an error in the moderation process"""
    pass

class PrincipleError(ThinkTankException):
    """Raised when there's an error related to principles"""
    pass

class ReflectionError(ThinkTankException):
    """Raised when there's an error in the reflection process"""
    pass

class PoolEvolutionError(ThinkTankException):
    """Raised when there's an error in the pool evolution process"""
    pass

class OutputGenerationError(ThinkTankException):
    """Raised when there's an error generating output"""
    pass

class ConfigurationError(ThinkTankException):
    """Raised when there's an error in the configuration"""
    pass

class VersionControlError(ThinkTankException):
    """Raised when there's an error in version control for principles and heuristics"""
    pass
    """Raised when there's an error in the pool evolution process"""
    pass
