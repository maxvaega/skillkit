"""Core module for skillkit library.

This module contains the framework-agnostic core functionality with zero
framework dependencies (stdlib + PyYAML only).
"""

from skillkit.core.discovery import SkillDiscovery
from skillkit.core.exceptions import (
    ArgumentProcessingError,
    ContentLoadError,
    InvalidFrontmatterError,
    InvalidYAMLError,
    MissingRequiredFieldError,
    SizeLimitExceededError,
    SkillInvocationError,
    SkillNotFoundError,
    SkillParsingError,
    SkillSecurityError,
    SkillsUseError,
    SuspiciousInputError,
)
from skillkit.core.manager import SkillManager
from skillkit.core.models import CacheStats, ContentCache, Skill, SkillMetadata
from skillkit.core.parser import SkillParser
from skillkit.core.processors import (
    ArgumentSubstitutionProcessor,
    BaseDirectoryProcessor,
    CompositeProcessor,
    ContentProcessor,
    normalize_arguments,
    process_skill_content,
)

__all__ = [
    # Core classes
    "SkillManager",
    "SkillMetadata",
    "Skill",
    "SkillDiscovery",
    "SkillParser",
    # Cache
    "ContentCache",
    "CacheStats",
    # Processors
    "ContentProcessor",
    "BaseDirectoryProcessor",
    "ArgumentSubstitutionProcessor",
    "CompositeProcessor",
    "normalize_arguments",
    "process_skill_content",
    # Exceptions
    "SkillsUseError",
    "SkillParsingError",
    "InvalidYAMLError",
    "MissingRequiredFieldError",
    "InvalidFrontmatterError",
    "SkillNotFoundError",
    "SkillInvocationError",
    "ArgumentProcessingError",
    "ContentLoadError",
    "SkillSecurityError",
    "SuspiciousInputError",
    "SizeLimitExceededError",
]
