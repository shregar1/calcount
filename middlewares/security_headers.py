from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""

    def __init__(
        self,
        app,
        content_security_policy: str = None,
        strict_transport_security: str = None,
        x_frame_options: str = "DENY",
        x_content_type_options: str = "nosniff",
        x_xss_protection: str = "1; mode=block",
        referrer_policy: str = "strict-origin-when-cross-origin",
        permissions_policy: str = None,
        enable_hsts: bool = True,
        enable_csp: bool = True,
        **kwargs,
    ):
        super().__init__(app)
        self.content_security_policy = (
            content_security_policy or self._get_default_csp()
        )
        self.strict_transport_security = (
            strict_transport_security or "max-age=31536000; includeSubDomains"
        )
        self.x_frame_options = x_frame_options
        self.x_content_type_options = x_content_type_options
        self.x_xss_protection = x_xss_protection
        self.referrer_policy = referrer_policy
        self.permissions_policy = (
            permissions_policy or self._get_default_permissions_policy()
        )
        self.enable_hsts = enable_hsts
        self.enable_csp = enable_csp

    def _get_default_csp(self) -> str:
        """Get default Content Security Policy."""
        return (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "upgrade-insecure-requests;"
        )

    def _get_default_permissions_policy(self) -> str:
        """Get default Permissions Policy."""
        return (
            "accelerometer=(), "
            "ambient-light-sensor=(), "
            "autoplay=(), "
            "battery=(), "
            "camera=(), "
            "cross-origin-isolated=(), "
            "display-capture=(), "
            "document-domain=(), "
            "encrypted-media=(), "
            "execution-while-not-rendered=(), "
            "execution-while-out-of-viewport=(), "
            "fullscreen=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "keyboard-map=(), "
            "magnetometer=(), "
            "microphone=(), "
            "midi=(), "
            "navigation-override=(), "
            "payment=(), "
            "picture-in-picture=(), "
            "publickey-credentials-get=(), "
            "screen-wake-lock=(), "
            "sync-xhr=(), "
            "usb=(), "
            "web-share=(), "
            "xr-spatial-tracking=()"
        )

    async def dispatch(self, request: Request, call_next):
        """Add security headers to the response."""
        response = await call_next(request)

        if self.enable_csp:
            response.headers["Content-Security-Policy"] = (
                self.content_security_policy
            )

        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                self.strict_transport_security
            )

        response.headers["X-Frame-Options"] = self.x_frame_options

        response.headers["X-Content-Type-Options"] = (
            self.x_content_type_options
        )

        response.headers["X-XSS-Protection"] = self.x_xss_protection

        response.headers["Referrer-Policy"] = self.referrer_policy

        response.headers["Permissions-Policy"] = self.permissions_policy

        response.headers["X-Download-Options"] = "noopen"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        if "Server" in response.headers:
            del response.headers["Server"]

        return response


class SecurityHeadersConfigDTO:
    """Configuration for security headers."""

    def __init__(
        self,
        enable_hsts: bool = True,
        enable_csp: bool = True,
        csp_report_only: bool = False,
        hsts_max_age: int = 31536000,  # 1 year
        hsts_include_subdomains: bool = True,
        hsts_preload: bool = False,
        frame_options: str = "DENY",
        content_type_options: str = "nosniff",
        xss_protection: str = "1; mode=block",
        referrer_policy: str = "strict-origin-when-cross-origin",
        custom_csp: str = None,
        custom_permissions_policy: str = None,
    ):
        self.enable_hsts = enable_hsts
        self.enable_csp = enable_csp
        self.csp_report_only = csp_report_only
        self.hsts_max_age = hsts_max_age
        self.hsts_include_subdomains = hsts_include_subdomains
        self.hsts_preload = hsts_preload
        self.frame_options = frame_options
        self.content_type_options = content_type_options
        self.xss_protection = xss_protection
        self.referrer_policy = referrer_policy
        self.custom_csp = custom_csp
        self.custom_permissions_policy = custom_permissions_policy

    def get_hsts_header(self) -> str:
        """Generate HSTS header value."""
        parts = [f"max-age={self.hsts_max_age}"]

        if self.hsts_include_subdomains:
            parts.append("includeSubDomains")

        if self.hsts_preload:
            parts.append("preload")

        return "; ".join(parts)

    def get_csp_header_name(self) -> str:
        """Get CSP header name (report-only or regular)."""
        return (
            "Content-Security-Policy-Report-Only"
            if self.csp_report_only
            else "Content-Security-Policy"
        )
