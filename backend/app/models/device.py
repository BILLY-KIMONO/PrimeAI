from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class DeviceProfile(Base, TimestampMixin):
    __tablename__ = "device_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Device configuration
    profile_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Device fingerprint spoofing
    user_agent = Column(Text, nullable=True)
    platform = Column(String(50), nullable=True)
    browser_vendor = Column(String(50), nullable=True)
    device_model = Column(String(100), nullable=True)
    os_version = Column(String(50), nullable=True)
    
    # Screen & Canvas spoofing
    screen_width = Column(Integer, nullable=True)
    screen_height = Column(Integer, nullable=True)
    screen_color_depth = Column(Integer, nullable=True)
    canvas_noise = Column(Boolean, default=True)
    webgl_noise = Column(Boolean, default=True)
    
    # Timezone & Language
    timezone = Column(String(50), nullable=True)
    language = Column(String(10), nullable=True)
    
    # Behavior settings
    random_mouse_movements = Column(Boolean, default=True)
    keyboard_delays = Column(Boolean, default=True)
    random_scroll_speed = Column(Boolean, default=True)
    
    # WebRTC & IP spoofing
    webrtc_leak_prevention = Column(Boolean, default=True)
    proxy_enabled = Column(Boolean, default=False)
    proxy_url = Column(Text, nullable=True)
    
    # Interview mode (maximum stealth)
    interview_mode = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="device_profiles")
    
    class Config:
        from_attributes = True
