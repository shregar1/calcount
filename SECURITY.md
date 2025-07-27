# Security Documentation

This document outlines the security features and best practices implemented in the CalCount application.

## Overview

The CalCount application implements multiple layers of security to protect against common web application vulnerabilities and ensure data integrity.

## Security Features

### 1. Enhanced Input Validation

#### Password Strength Validation
- **Minimum Requirements**: 8 characters minimum
- **Complexity Requirements**: 
  - At least one lowercase letter
  - At least one uppercase letter
  - At least one digit
  - At least one special character (@$!%*?&)
- **Additional Checks**:
  - No more than 2 consecutive identical characters
  - Protection against common weak passwords
  - Maximum length enforcement

#### Email Validation
- **Format Validation**: Uses `email-validator` library for comprehensive email format checking
- **Normalization**: Automatically normalizes email addresses
- **Length Limits**: Maximum 254 characters

#### String Sanitization
- **Control Character Removal**: Removes null bytes and control characters
- **Length Limits**: Configurable maximum string length (default: 1000 characters)
- **Whitespace Handling**: Proper trimming and normalization

#### Security Validation
- **SQL Injection Prevention**: Pattern-based detection of SQL injection attempts
- **XSS Prevention**: Detection of script tags and dangerous HTML
- **Path Traversal Prevention**: Protection against directory traversal attacks

### 2. Enhanced Rate Limiting

#### Multiple Strategies
- **Sliding Window**: Most accurate rate limiting with configurable windows
- **Fixed Window**: Simple time-based rate limiting
- **Token Bucket**: Burst-friendly rate limiting for API endpoints

#### Configuration
- **Per-Minute Limits**: Configurable requests per minute (default: 60)
- **Per-Hour Limits**: Configurable requests per hour (default: 1000)
- **Burst Limits**: Configurable burst capacity (default: 10)
- **Excluded Paths**: Health checks, documentation, and OPTIONS requests

#### Features
- **Client Identification**: Uses X-Forwarded-For, X-Real-IP, or client host
- **Automatic Cleanup**: Periodic cleanup of old rate limiting data
- **Detailed Headers**: X-RateLimit-* headers for client information
- **Graceful Degradation**: Proper error responses with retry information

### 3. Security Headers

#### HTTP Strict Transport Security (HSTS)
- **Max Age**: 1 year (31536000 seconds)
- **Include Subdomains**: Enabled
- **Preload**: Configurable

#### Content Security Policy (CSP)
- **Default Policy**: Restrictive policy preventing XSS and injection attacks
- **Report-Only Mode**: Configurable for testing
- **Custom Policies**: Support for custom CSP rules

#### Additional Headers
- **X-Frame-Options**: DENY (prevents clickjacking)
- **X-Content-Type-Options**: nosniff (prevents MIME type sniffing)
- **X-XSS-Protection**: 1; mode=block (legacy XSS protection)
- **Referrer-Policy**: strict-origin-when-cross-origin
- **Permissions-Policy**: Comprehensive feature restrictions

### 4. Authentication & Authorization

#### JWT Token Security
- **Expiration**: Configurable token expiry (default: 30 minutes)
- **Secure Storage**: Tokens stored securely in memory
- **Session Management**: Proper session timeout and cleanup

#### Password Security
- **Strong Password Requirements**: Enforced through validation
- **Password History**: Configurable password history (default: 5)
- **Account Lockout**: Protection against brute force attacks
- **Session Timeout**: Automatic session expiration

## Configuration

### Environment Variables

The following environment variables can be used to configure security settings:

```bash
# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_REQUESTS_PER_HOUR=1000
RATE_LIMIT_BURST_LIMIT=10

# Security Headers
SECURITY_HSTS_MAX_AGE=31536000
SECURITY_HSTS_INCLUDE_SUBDOMAINS=true
SECURITY_ENABLE_CSP=true
SECURITY_ENABLE_HSTS=true

# Input Validation
SECURITY_MAX_STRING_LENGTH=1000
SECURITY_MIN_PASSWORD_LENGTH=8

# Authentication
SECURITY_JWT_EXPIRY_MINUTES=30
SECURITY_MAX_LOGIN_ATTEMPTS=5
```

### Configuration File

Security settings can also be configured through the JSON configuration file at `config/security/config.json`.

## Security Best Practices

### 1. Input Validation
- Always validate and sanitize all user inputs
- Use the enhanced validation utilities for consistent validation
- Implement proper error handling for validation failures

### 2. Rate Limiting
- Configure appropriate rate limits for your use case
- Monitor rate limiting logs for potential abuse
- Adjust limits based on application performance and user needs

### 3. Security Headers
- Keep security headers enabled in production
- Test CSP policies in report-only mode before enforcing
- Regularly review and update security policies

### 4. Authentication
- Use strong password requirements
- Implement proper session management
- Monitor for suspicious authentication patterns

### 5. Data Protection
- Encrypt sensitive data at rest and in transit
- Use HTTPS in production environments
- Implement proper access controls

## Security Testing

### Running Security Tests

```bash
# Run all security-related tests
pytest tests/utilities/test_validation.py -v

# Run specific test categories
pytest tests/utilities/test_validation.py::TestValidationUtility -v
pytest tests/utilities/test_validation.py::TestSecurityValidators -v
pytest tests/utilities/test_validation.py::TestEnhancedBaseModel -v
```

### Test Coverage

The security tests cover:
- Password strength validation
- Email format validation
- UUID format validation
- Date range validation
- String sanitization
- SQL injection prevention
- XSS prevention
- Path traversal prevention
- Enhanced base model functionality

## Monitoring & Logging

### Security Events
- Rate limit violations are logged with client information
- Authentication failures are tracked
- Input validation failures are recorded
- Security header violations are monitored

### Log Analysis
- Monitor for unusual patterns in authentication attempts
- Track rate limiting violations by client
- Review security validation failures
- Analyze CSP violation reports (if enabled)

## Incident Response

### Rate Limiting Violations
1. Monitor rate limiting logs
2. Identify patterns of abuse
3. Adjust rate limits if necessary
4. Block malicious IPs if required

### Security Validation Failures
1. Review failed validation attempts
2. Investigate potential attack patterns
3. Update validation rules if needed
4. Monitor for similar attempts

### Authentication Issues
1. Review authentication failure logs
2. Check for brute force attempts
3. Implement additional security measures if needed
4. Consider account lockout policies

## Compliance

### GDPR Compliance
- Data minimization through input validation
- Secure data transmission with security headers
- Proper session management and data retention

### OWASP Top 10 Protection
- **A01:2021 - Broken Access Control**: Proper authentication and authorization
- **A02:2021 - Cryptographic Failures**: HTTPS and secure headers
- **A03:2021 - Injection**: Input validation and sanitization
- **A04:2021 - Insecure Design**: Security by design principles
- **A05:2021 - Security Misconfiguration**: Proper security headers
- **A06:2021 - Vulnerable Components**: Regular dependency updates
- **A07:2021 - Authentication Failures**: Strong authentication measures
- **A08:2021 - Software and Data Integrity**: Input validation
- **A09:2021 - Security Logging**: Comprehensive security logging
- **A10:2021 - SSRF**: Input validation and sanitization

## Updates & Maintenance

### Regular Updates
- Keep dependencies updated
- Review and update security configurations
- Monitor security advisories
- Update validation rules as needed

### Security Audits
- Regular security code reviews
- Penetration testing
- Vulnerability assessments
- Compliance audits

## Support

For security-related issues or questions:
1. Review this documentation
2. Check the security configuration
3. Review security test results
4. Contact the development team

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/) 