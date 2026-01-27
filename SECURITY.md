# Security Policy

## Security Improvements

This document outlines the security enhancements implemented in the YouTube automation system.

### 1. Credential Storage

**Issue**: Credentials were stored in the project root directory, risking exposure to version control.

**Solution**: 
- All credentials are now stored in a secure user directory: `~/.youtube_automation/credentials/`
- Directory permissions are set to `0o700` (owner read/write/execute only)
- Files include:
  - `token.pickle` - YouTube OAuth token
  - Moved from project root to secure location

**Files Modified**: `youtube_uploader.py`, `utils.py`

### 2. Temporary File Security

**Issue**: Temporary files were created in a world-readable `temp/` directory.

**Solution**:
- Use Python's `tempfile.mkdtemp()` to create secure temporary directories
- Permissions set to `0o700` (owner-only access)
- Temporary audio and video files are protected from unauthorized access

**Files Modified**: `video_creator.py`

### 3. API Key Validation

**Issue**: API keys were accepted without validation, potentially causing unclear error messages.

**Solution**:
- Added `validate_api_key()` function in `utils.py`
- Validates that API keys are:
  - Not None
  - Not empty strings
  - Properly stripped of whitespace
- Provides clear error messages when validation fails

**Files Modified**: `content_generator.py`, `utils.py`

### 4. Input Validation

**Issue**: Configuration updates accepted any keys without validation.

**Solution**:
- Implemented whitelist of allowed configuration keys in `config.py`
- Only `content_topic`, `content_frequency`, and `video_privacy` can be updated via API
- Sensitive configuration like API keys cannot be modified through the web interface
- Returns error message for invalid update attempts

**Files Modified**: `config.py`, `app.py`

### 5. Exception Handling

**Issue**: Broad exception handlers could mask errors and leak sensitive information.

**Solution**:
- Added specific exception types where appropriate:
  - `openai.APIError` for OpenAI API errors
  - `googleapiclient.errors.HttpError` for YouTube API errors
  - `json.JSONDecodeError` for JSON parsing errors
- Sanitized error messages to avoid leaking sensitive information
- Improved error context for debugging

**Files Modified**: `content_generator.py`, `youtube_uploader.py`

### 6. Configuration Management

**Issue**: Configuration was duplicated and scattered across files.

**Solution**:
- Centralized configuration in `config.py`
- Sensitive data (API keys) excluded from API responses
- `to_dict()` method provides safe configuration without secrets
- Validation on initialization and updates

**Files Modified**: `config.py`, `app.py`

## Security Best Practices

### For Users

1. **Never commit credentials**:
   - `.env` file contains API keys - keep it out of version control
   - `client_secrets.json` is git-ignored automatically
   - Credentials are stored in `~/.youtube_automation/` (outside project)

2. **Environment Variables**:
   - Always use `.env` file for sensitive configuration
   - Never hardcode API keys in source code
   - Use `.env.example` as a template

3. **File Permissions**:
   - Ensure `~/.youtube_automation/` has restricted permissions
   - On Unix systems: `chmod 700 ~/.youtube_automation`

4. **API Keys**:
   - Rotate API keys regularly
   - Use separate keys for development and production
   - Revoke keys immediately if compromised

### For Developers

1. **Adding New Features**:
   - Always validate user input
   - Use specific exception types
   - Don't log sensitive information
   - Store credentials in secure locations

2. **Configuration Changes**:
   - Add new config keys to `Config.UPDATABLE_KEYS` whitelist if they should be user-modifiable
   - Keep sensitive keys out of the whitelist
   - Document configuration options

3. **Error Handling**:
   - Catch specific exceptions before generic ones
   - Provide helpful error messages without exposing internal details
   - Log errors appropriately (avoid logging secrets)

## Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do NOT** open a public GitHub issue
2. Email the maintainers directly with details
3. Allow time for the issue to be addressed before public disclosure

## Security Checklist

- [x] Credentials stored in secure user directory
- [x] Temporary files use secure permissions
- [x] API keys validated on initialization
- [x] Input validation for configuration updates
- [x] Specific exception handling
- [x] Sensitive data excluded from API responses
- [x] `.gitignore` includes credential files
- [ ] Rate limiting for API endpoints (future enhancement)
- [ ] HTTPS enforcement in production (deployment-specific)
- [ ] Regular dependency updates for security patches

## Additional Notes

### Cache Security

- Cache files are stored in `.cache/` directory
- Cache directory has restricted permissions (`0o700`)
- Cache contains only API responses, no credentials
- Cache automatically expires based on TTL settings

### History File

- `automation_history.json` is git-ignored
- Contains metadata about video creation runs
- Does not store API keys or credentials
- Stored in project directory with standard file permissions
