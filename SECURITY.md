# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

## Reporting Security Vulnerabilities

**Please do not open public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability, please report it by email to the project maintainers:
- Tanvi Gode
- Astha Singh
- Gayatri Tasalwar

Include the following information:
1. Type of vulnerability
2. Location of affected code
3. Steps to reproduce
4. Potential impact
5. Suggested fix (if available)

## Security Best Practices

This project follows these security practices:

- ✅ Input validation on all URL inputs
- ✅ No sensitive credentials in code
- ✅ Environment variables for configuration
- ✅ Trusted domain whitelist validation
- ✅ Model verification (when available)
- ✅ Regular dependency updates
- ✅ Secure default configurations

## Known Limitations

- URLs are not logged for privacy, but consider this in production
- Models are downloaded from external sources (verify checksums)
- HTTPS is recommended for production deployments

## Vulnerability Disclosure

Once a vulnerability is reported:
1. We'll acknowledge receipt within 48 hours
2. We'll work on a fix promptly
3. We'll notify reporters once patched
4. We'll publish a security advisory

Thank you for helping us keep this project secure!
