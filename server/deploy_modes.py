"""HTTPS deployment presets for AISignX server config."""

from __future__ import annotations

MODES: dict[str, dict] = {
    'https': {
        'label': 'HTTPS (Caddy / nginx / IIS on 443)',
        'description': (
            'Terminate TLS at Caddy, nginx, or IIS. AISignX listens on '
            'http://127.0.0.1:5000 behind the proxy. Browser clients require '
            'this mode for offline caching.'
        ),
        'trust_proxy': True,
        'proxy_hops': 1,
        'preferred_url_scheme': 'https',
        'session_cookie_secure': True,
        'remember_cookie_secure': True,
        'client_url_template': 'https://{host}',
    },
}


def normalize_mode(mode: str | None) -> str:
    value = (mode or 'https').strip().lower()
    if value == 'http':
        # Legacy configs — AISignX is HTTPS-only for clients
        value = 'https'
    if value not in MODES:
        allowed = ', '.join(sorted(MODES))
        raise ValueError(f"Unknown deploy mode {mode!r}. Use one of: {allowed}")
    return value


def resolve_deploy_settings(
    mode: str | None,
    *,
    proxy_hops: int | None = None,
    server_name: str | None = None,
) -> dict:
    """Return config.py-ready settings for HTTPS deployment."""
    key = normalize_mode(mode)
    preset = MODES[key]
    hops = int(proxy_hops if proxy_hops is not None else preset['proxy_hops'])
    hostname = (server_name or '').strip() or None
    return {
        'AISIGNX_DEPLOY_MODE': key,
        'TRUST_PROXY': preset['trust_proxy'],
        'TRUST_PROXY_HOPS': hops,
        'PREFERRED_URL_SCHEME': preset['preferred_url_scheme'],
        'SESSION_COOKIE_SECURE': preset['session_cookie_secure'],
        'REMEMBER_COOKIE_SECURE': preset['remember_cookie_secure'],
        'SERVER_NAME': hostname,
    }


def client_url_hint(mode: str | None, server_name: str | None = None) -> str:
    key = normalize_mode(mode)
    host = (server_name or '').strip() or 'YOUR_HOST'
    return MODES[key]['client_url_template'].format(host=host)


def describe_mode(mode: str | None) -> str:
    key = normalize_mode(mode)
    preset = MODES[key]
    return f"{key}: {preset['label']} - {preset['description']}"
