"""HTTPS-only URL helpers for client setup and public URLs."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse


def normalize_https_base_url(url: str) -> str:
    """Return a base URL forced to https with no trailing slash."""
    raw = (url or '').strip()
    if not raw:
        return ''
    if not raw.startswith(('http://', 'https://')):
        raw = 'https://' + raw.lstrip('/')
    parsed = urlparse(raw)
    host = parsed.hostname or parsed.netloc or ''
    if not host:
        return ''
    port = parsed.port
    # Default ports — omit from URL we give clients
    if port in (None, 443):
        netloc = host
    elif port == 80:
        netloc = host
    else:
        netloc = f'{host}:{port}'
    return urlunparse(('https', netloc, '', '', '', '')).rstrip('/')


def validate_https_client_url(url: str) -> tuple[bool, str]:
    """Validate a server URL for native/browser clients (HTTPS only)."""
    raw = (url or '').strip()
    if not raw:
        return False, 'Server URL is required.'
    if raw.lower().startswith('http://'):
        return False, 'HTTP is not supported. Use https:// (port 443, or https://host:8443).'
    normalized = normalize_https_base_url(raw)
    if not normalized.startswith('https://'):
        return False, 'URL must use https://'
    parsed = urlparse(normalized)
    if not parsed.hostname:
        return False, 'Invalid server hostname.'
    return True, normalized
