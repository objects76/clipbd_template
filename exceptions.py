#!/usr/bin/env python3
"""Custom exceptions for the clipboard template system.

This module defines a hierarchy of custom exceptions used throughout
the clipboard template application to provide better error handling
and more specific error information.
"""


class ClipboardTemplateError(Exception):
    """Base exception for all clipboard template system errors."""
    pass


class ClipboardError(ClipboardTemplateError):
    """Base exception for clipboard-related operations."""
    pass


class ContentNotFoundError(ClipboardError):
    """Raised when no valid clipboard content is found."""
    pass


class ContentExtractionError(ClipboardTemplateError):
    """Base exception for content extraction failures."""
    pass


class YouTubeExtractionError(ContentExtractionError):
    """Raised when YouTube transcript extraction fails."""
    pass


class WebExtractionError(ContentExtractionError):
    """Raised when web content extraction fails."""
    pass


class MediumExtractionError(ContentExtractionError):
    """Raised when Medium article extraction fails."""
    pass


class TemplateError(ClipboardTemplateError):
    """Base exception for template system errors."""
    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a template file or template choice is not found."""
    pass


class TemplateFormatError(TemplateError):
    """Raised when template format is invalid."""
    pass


class APIError(ClipboardTemplateError):
    """Base exception for external API errors."""
    pass


class JinaAPIError(APIError):
    """Raised when Jina Reader API operations fail."""
    pass


class FirecrawlAPIError(APIError):
    """Raised when Firecrawl API operations fail."""
    pass


class ConfigurationError(ClipboardTemplateError):
    """Raised when configuration is missing or invalid."""
    pass


class SystemDependencyError(ClipboardTemplateError):
    """Raised when required system dependencies are missing."""
    pass