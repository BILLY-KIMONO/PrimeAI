"""
PrimeAI Extension Configuration
Generated for production deployment
"""

CONFIG = {
    # API Settings
    "api": {
        "url": "https://api.primeai.com",
        "timeout": 30,
        "retry_attempts": 3,
        "retry_delay": 1000
    },
    
    # Subscription
    "subscription": {
        "trial_days": 1,
        "monthly_price_usd": 8,
        "monthly_price_kes": 1000,
        "api_calls_limit": 1000,
    },
    
    # Security
    "security": {
        "encryption": "AES-256",
        "token_expiry": "30d",
        "max_inactive_time": "24h",
        "require_password_reset_days": 90
    },
    
    # Anti-Detect Features
    "antidetect": {
        "canvas_noise": True,
        "webgl_noise": True,
        "webrtc_leak_prevention": True,
        "devtools_detection_bypass": True,
        "browser_fingerprint_spoofing": True,
        "behavior_randomization": True
    },
    
    # Interview Mode
    "interview_mode": {
        "enabled": True,
        "max_stealth_level": 10,
        "devtools_blocker": True,
        "right_click_blocker": True,
        "keyboard_shortcut_blocker": True,
        "console_blocker": True
    },
    
    # Performance
    "performance": {
        "cache_profiles": True,
        "cache_ttl": 86400,
        "lazy_load_scripts": True,
        "compression": "gzip"
    },
    
    # Logging
    "logging": {
        "level": "INFO",
        "enable_error_reporting": True,
        "sentry_dsn": "https://key@sentry.io/project"
    }
}
