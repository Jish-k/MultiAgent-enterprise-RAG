from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os

from database.postgres import get_db
from database.models import User, OTPRecord
from .models import LoginRequest, VerifyOTPRequest, TokenResponse
from .otp import generate_otp, hash_otp, verify_otp_hash
from .jwt_handler import create_access_token, get_current_user
from .email_service import send_otp_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(request: LoginRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        user = User(email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)

    db.query(OTPRecord).filter(OTPRecord.email == request.email).delete()

    otp = generate_otp()
    hashed = hash_otp(otp)
    expires = datetime.utcnow() + timedelta(minutes=5)
    
    record = OTPRecord(email=request.email, hashed_otp=hashed, expires_at=expires)
    db.add(record)
    db.commit()
    
    background_tasks.add_task(send_otp_email, request.email, otp)
    
    return {"message": "OTP sent to email successfully"}

@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    record = db.query(OTPRecord).filter(OTPRecord.email == request.email).first()
    
    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    if record.expires_at < datetime.utcnow():
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")
        
    if not verify_otp_hash(request.otp, record.hashed_otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    user = db.query(User).filter(User.email == request.email).first()
    
    db.delete(record)
    db.commit()
    
    access_token = create_access_token(data={"sub": user.email, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    admin_email = os.getenv("SMTP_USER", "")
    is_admin = current_user.get("sub") == admin_email
    return {"user": current_user, "is_admin": is_admin}
