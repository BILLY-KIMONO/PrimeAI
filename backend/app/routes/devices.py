from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models.device import DeviceProfile
from app.models.user import User
from app.services import verify_token

router = APIRouter()

class DeviceProfileRequest(BaseModel):
    profile_name: str
    description: Optional[str] = None
    user_agent: Optional[str] = None
    browser_vendor: Optional[str] = None
    device_model: Optional[str] = None
    screen_width: Optional[int] = None
    screen_height: Optional[int] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    interview_mode: bool = True
    random_mouse_movements: bool = True
    keyboard_delays: bool = True
    canvas_noise: bool = True
    webgl_noise: bool = True
    webrtc_leak_prevention: bool = True

class DeviceProfileResponse(BaseModel):
    id: int
    profile_name: str
    interview_mode: bool
    is_active: bool
    
    class Config:
        from_attributes = True

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

@router.post("/create")
def create_device_profile(
    req: DeviceProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new device profile"""
    profile = DeviceProfile(
        user_id=current_user.id,
        **req.dict()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return DeviceProfileResponse.from_orm(profile)

@router.get("/list")
def list_device_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all device profiles"""
    profiles = db.query(DeviceProfile).filter(
        DeviceProfile.user_id == current_user.id
    ).all()
    
    return [DeviceProfileResponse.from_orm(p) for p in profiles]

@router.get("/{profile_id}")
def get_device_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific device profile with full details"""
    profile = db.query(DeviceProfile).filter(
        DeviceProfile.id == profile_id,
        DeviceProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile

@router.put("/{profile_id}")
def update_device_profile(
    profile_id: int,
    req: DeviceProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update device profile"""
    profile = db.query(DeviceProfile).filter(
        DeviceProfile.id == profile_id,
        DeviceProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in req.dict().items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    
    return DeviceProfileResponse.from_orm(profile)

@router.delete("/{profile_id}")
def delete_device_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete device profile"""
    profile = db.query(DeviceProfile).filter(
        DeviceProfile.id == profile_id,
        DeviceProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    
    return {"message": "Profile deleted"}
