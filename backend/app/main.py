from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import settings

def create_app():
    app = FastAPI(
        title="PrimeAI Anti-Detect",
        description="Production-ready anti-detect browser extension",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "*.primeai.com"]
    )
    
    # Include routes
    from app.routes import auth, subscriptions, devices, extension
    
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
    app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
    app.include_router(extension.router, prefix="/api/extension", tags=["extension"])
    
    @app.get("/health")
    def health():
        return {"status": "ok"}
    
    return app

app = create_app()
