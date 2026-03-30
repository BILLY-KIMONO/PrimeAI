import uvicorn
from app.main import app
from app.database import init_db

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Run server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
