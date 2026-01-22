#!/usr/bin/env python3
"""Custom exceptions for the clipboard template system.

This module defines a hierarchy of custom exceptions used throughout
the clipboard template application to provide better error handling
and more specific error information.
"""


class ClipboardTemplateError(Exception):
    """Base exception for all clipboard template system errors."""


class ClipboardError(ClipboardTemplateError):
    """Base exception for clipboard-related operations."""


class ContentNotFoundError(ClipboardError):
    """Raised when no valid clipboard content is found."""


class ContentExtractionError(ClipboardTemplateError):
    """Base exception for content extraction failures."""


class YouTubeExtractionError(ContentExtractionError):
    """Raised when YouTube transcript extraction fails."""


class WebExtractionError(ContentExtractionError):
    """Raised when web content extraction fails."""


class MediumExtractionError(ContentExtractionError):
    """Raised when Medium article extraction fails."""


class TemplateError(ClipboardTemplateError):
    """Base exception for template system errors."""


class TemplateNotFoundError(TemplateError):
    """Raised when a template file or template choice is not found."""


class TemplateFormatError(TemplateError):
    """Raised when template format is invalid."""


class APIError(ClipboardTemplateError):
    """Base exception for external API errors."""


class JinaAPIError(APIError):
    """Raised when Jina Reader API operations fail."""


class FirecrawlAPIError(APIError):
    """Raised when Firecrawl API operations fail."""


class ConfigurationError(ClipboardTemplateError):
    """Raised when configuration is missing or invalid."""


class SystemDependencyError(ClipboardTemplateError):
    """Raised when required system dependencies are missing."""
