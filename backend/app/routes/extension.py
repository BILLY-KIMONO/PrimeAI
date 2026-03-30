from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.device import DeviceProfile
from app.services import verify_token
from app.services.subscription import has_api_calls_remaining, increment_api_calls

router = APIRouter()

class ExtensionConfigRequest(BaseModel):
    profile_id: int

class ExtensionConfigResponse(BaseModel):
    user_agent: str
    platform: str
    device_model: str
    screen_width: int
    screen_height: int
    screen_color_depth: int
    timezone: str
    language: str
    canvas_noise: bool
    webgl_noise: bool
    random_mouse_movements: bool
    keyboard_delays: bool
    random_scroll_speed: bool
    webrtc_leak_prevention: bool
    interview_mode: bool

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Extract and validate user from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/config")
def get_extension_config(
    req: ExtensionConfigRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get anti-detect configuration for extension"""
    
    # Check subscription
    if not has_api_calls_remaining(db, current_user.id):
        raise HTTPException(status_code=403, detail="API calls limit exceeded")
    
    # Get device profile
    profile = db.query(DeviceProfile).filter(
        DeviceProfile.id == req.profile_id,
        DeviceProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Increment API calls
    increment_api_calls(db, current_user.id)
    
    return {
        "user_agent": profile.user_agent,
        "platform": profile.platform,
        "device_model": profile.device_model,
        "screen_width": profile.screen_width,
        "screen_height": profile.screen_height,
        "screen_color_depth": profile.screen_color_depth,
        "timezone": profile.timezone,
        "language": profile.language,
        "canvas_noise": profile.canvas_noise,
        "webgl_noise": profile.webgl_noise,
        "random_mouse_movements": profile.random_mouse_movements,
        "keyboard_delays": profile.keyboard_delays,
        "random_scroll_speed": profile.random_scroll_speed,
        "webrtc_leak_prevention": profile.webrtc_leak_prevention,
        "interview_mode": profile.interview_mode
    }

@router.post("/validate")
def validate_extension(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Validate extension is active and has access"""
    from app.services.subscription import is_subscription_active
    
    if not is_subscription_active(db, current_user.id):
        raise HTTPException(status_code=403, detail="Subscription expired")
    
    return {"valid": True, "message": "Extension is active"}
