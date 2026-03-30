"""
PrimeAI API Documentation
Complete reference guide for all endpoints
"""

# ============================================================
# AUTHENTICATION ENDPOINTS
# ============================================================

POST /api/auth/register
"""
Register new user with 1-day free trial

Request:
{
    "email": "user@example.com",
    "username": "john_dev",
    "password": "SecurePassword123!"
}

Response (201):
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "john_dev"
    }
}

Errors:
- 400: Email already registered
- 422: Invalid email format or weak password
"""

POST /api/auth/login
"""
Login with email and password

Request:
{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}

Response (200):
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "john_dev"
    }
}

Errors:
- 401: Invalid credentials
- 404: User not found
"""

GET /api/auth/me
"""
Get current authenticated user

Headers:
Authorization: Bearer {token}

Response (200):
{
    "id": 1,
    "email": "user@example.com",
    "username": "john_dev",
    "is_active": true
}

Errors:
- 401: Not authenticated
- 404: User not found
"""

# ============================================================
# DEVICE PROFILE ENDPOINTS
# ============================================================

POST /api/devices/create
"""
Create new device profile

Headers:
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
    "profile_name": "Interview Mode",
    "description": "Maximum stealth for interviews",
    "user_agent": "Mozilla/5.0...",
    "browser_vendor": "Google Inc.",
    "device_model": "Generic PC",
    "screen_width": 1920,
    "screen_height": 1080,
    "timezone": "America/New_York",
    "language": "en-US",
    "interview_mode": true,
    "random_mouse_movements": true,
    "keyboard_delays": true,
    "canvas_noise": true,
    "webgl_noise": true,
    "webrtc_leak_prevention": true
}

Response (201):
{
    "id": 5,
    "profile_name": "Interview Mode",
    "interview_mode": true,
    "is_active": true
}

Errors:
- 401: Not authenticated
- 422: Invalid data
"""

GET /api/devices/list
"""
List all device profiles for user

Headers:
Authorization: Bearer {token}

Response (200):
[
    {
        "id": 1,
        "profile_name": "Interview Mode",
        "interview_mode": true,
        "is_active": true
    },
    {
        "id": 2,
        "profile_name": "Regular Browse",
        "interview_mode": false,
        "is_active": true
    }
]

Errors:
- 401: Not authenticated
"""

GET /api/devices/{profile_id}
"""
Get specific device profile details

Headers:
Authorization: Bearer {token}

Response (200):
{
    "id": 1,
    "user_id": 1,
    "profile_name": "Interview Mode",
    "user_agent": "Mozilla/5.0...",
    "platform": "Linux x86_64",
    "device_model": "Generic PC",
    "screen_width": 1920,
    "screen_height": 1080,
    "screen_color_depth": 24,
    "timezone": "America/New_York",
    "language": "en-US",
    "random_mouse_movements": true,
    "keyboard_delays": true,
    "canvas_noise": true,
    "webgl_noise": true,
    "webrtc_leak_prevention": true,
    "interview_mode": true,
    "is_active": true
}

Errors:
- 401: Not authenticated
- 404: Profile not found
"""

PUT /api/devices/{profile_id}
"""
Update device profile

Headers:
Authorization: Bearer {token}
Content-Type: application/json

Response (200): Updated profile object

Errors:
- 401: Not authenticated
- 404: Profile not found
"""

DELETE /api/devices/{profile_id}
"""
Delete device profile

Headers:
Authorization: Bearer {token}

Response (200):
{
    "message": "Profile deleted"
}

Errors:
- 401: Not authenticated
- 404: Profile not found
"""

# ============================================================
# ANTI-DETECT / EXTENSION ENDPOINTS
# ============================================================

POST /api/extension/config
"""
Get anti-detect configuration for extension

Headers:
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
    "profile_id": 1
}

Response (200):
{
    "user_agent": "Mozilla/5.0...",
    "platform": "Linux x86_64",
    "device_model": "Generic PC",
    "screen_width": 1920,
    "screen_height": 1080,
    "screen_color_depth": 24,
    "timezone": "America/New_York",
    "language": "en-US",
    "canvas_noise": true,
    "webgl_noise": true,
    "random_mouse_movements": true,
    "keyboard_delays": true,
    "random_scroll_speed": true,
    "webrtc_leak_prevention": true,
    "interview_mode": true
}

Usage:
- Called by extension when loading pages
- Increments API call count
- Returns config to inject into page

Errors:
- 401: Not authenticated
- 403: Subscription expired or API limits exceeded
- 404: Profile not found
"""

POST /api/extension/validate
"""
Validate extension access and subscription

Headers:
Authorization: Bearer {token}

Response (200):
{
    "valid": true,
    "message": "Extension is active"
}

Response (403):
{
    "detail": "Subscription expired"
}

Usage:
- Called by extension periodically to check validity
- Used for license verification

Errors:
- 401: Not authenticated
- 403: Subscription expired
"""

# ============================================================
# SUBSCRIPTION ENDPOINTS
# ============================================================

GET /api/subscriptions/active
"""
Get current active subscription

Headers:
Authorization: Bearer {token}

Response (200):
{
    "id": 1,
    "plan_type": "trial",
    "start_date": "2026-03-30T10:00:00",
    "end_date": "2026-03-31T10:00:00",
    "is_active": true,
    "api_calls_used": 45,
    "api_calls_limit": 1000
}

Errors:
- 401: Not authenticated
- 404: No active subscription
"""

GET /api/subscriptions/list
"""
List all subscriptions (past and current)

Headers:
Authorization: Bearer {token}

Response (200):
[
    {
        "id": 1,
        "plan_type": "trial",
        "start_date": "2026-03-30T10:00:00",
        "end_date": "2026-03-31T10:00:00",
        "is_active": false,
        "api_calls_used": 1000,
        "api_calls_limit": 1000
    },
    {
        "id": 2,
        "plan_type": "monthly",
        "start_date": "2026-03-31T10:00:00",
        "end_date": "2026-04-30T10:00:00",
        "is_active": true,
        "api_calls_used": 45,
        "api_calls_limit": 1000
    }
]

Errors:
- 401: Not authenticated
"""

POST /api/subscriptions/cancel
"""
Cancel active subscription

Headers:
Authorization: Bearer {token}

Response (200):
{
    "message": "Subscription cancelled"
}

Errors:
- 401: Not authenticated
- 404: No active subscription
"""

# ============================================================
# ERROR CODES
# ============================================================

"""
200 OK: Request successful
201 Created: Resource created successfully
400 Bad Request: Invalid request data
401 Unauthorized: Missing or invalid authentication
403 Forbidden: Insufficient permissions or expired subscription
404 Not Found: Resource not found
422 Unprocessable Entity: Invalid data format
429 Too Many Requests: Rate limit exceeded
500 Internal Server Error: Server error
503 Service Unavailable: Maintenance
"""

# ============================================================
# AUTHENTICATION
# ============================================================

"""
All protected endpoints require Authorization header:

Authorization: Bearer {access_token}

Bearer token format: JWT with 3 parts separated by dots
Example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIn0.xyz...

Token expiry: 30 days (from login)
Refresh: Login again to get new token
"""

# ============================================================
# RATE LIMITING
# ============================================================

"""
API Rate Limits (per user):
- 100 requests per minute (most endpoints)
- 1,000 API calls per month (extension/config endpoint)

Headers returned:
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000

When limit exceeded: 429 Too Many Requests
"""

# ============================================================
# PRICING REFERENCE
# ============================================================

"""
PRICING TIERS:

Trial Plan (Free - 1 Day)
- API Calls: 1,000/month
- Profiles: Unlimited
- Features: All included
- Cost: $0

Monthly Plan
- API Calls: 1,000/month
- Profiles: Unlimited
- Features: All included
- Cost: $8 USD (~1,000 KES)

Per-API-Call Calculation:
- 1,000 calls/month = 0.008 USD per call
- Monthly plan = lowest cost per call
"""

# ============================================================
# USAGE EXAMPLES
# ============================================================

"""
EXAMPLE 1: Full Sign-Up Flow

1. Register
POST /api/auth/register
{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "SecurePass123!"
}
→ Get access_token
→ Auto-created trial subscription (1 day free)

2. Create Device Profile
POST /api/devices/create
Header: Authorization: Bearer {token}
{
    "profile_name": "Interview Mode",
    "screen_width": 1920,
    "screen_height": 1080,
    "timezone": "America/New_York",
    "interview_mode": true
}
→ Get profile_id

3. Install Browser Extension
- Load unpacked from extension/ folder
- Extension connects with token
- User selects profile from extension popup

4. Fetch Configuration
POST /api/extension/config
Header: Authorization: Bearer {token}
{
    "profile_id": 1
}
→ Extension receives anti-detect config
→ Config injected into pages
→ API call count incremented


EXAMPLE 2: Login With Existing Account

1. Login
POST /api/auth/login
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
→ Get access_token

2. Check Active Subscription
GET /api/subscriptions/active
Header: Authorization: Bearer {token}
→ Verify plan is active and days remaining

3. Load Stored Profile
GET /api/devices/list
Header: Authorization: Bearer {token}
→ Get all available profiles

4. Use Extension
- Extension sends stored access_token
- Gets profile config
- Applies anti-detect settings
"""
