from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Robot(Base):
    __tablename__ = "robots"

    id = Column(String, primary_key=True)
    name = Column(String)
    status = Column(String)
    battery_level = Column(Integer)
    last_active = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # 센서 데이터 관계 설정
    sensor_data = relationship("SensorData", back_populates="robot")
    camera_data = relationship("CameraData", back_populates="robot")

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, ForeignKey("robots.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # LiDAR 데이터
    lidar_points = Column(String)  # JSON 형식으로 저장
    
    # IMU 데이터
    acceleration_x = Column(Float)
    acceleration_y = Column(Float)
    acceleration_z = Column(Float)
    gyro_x = Column(Float)
    gyro_y = Column(Float)
    gyro_z = Column(Float)
    
    # 위치 데이터
    position_x = Column(Float)
    position_y = Column(Float)
    orientation = Column(Float)
    
    robot = relationship("Robot", back_populates="sensor_data")

class CameraData(Base):
    __tablename__ = "camera_data"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, ForeignKey("robots.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    frame_number = Column(Integer)
    image_data = Column(String)  # Base64 인코딩된 이미지 데이터
    
    robot = relationship("Robot", back_populates="camera_data") 