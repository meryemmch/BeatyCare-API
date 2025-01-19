from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.user import UserSchema
import models.users
from models.users import User, RoleEnum
from auth import create_access_token, get_current_user, get_password_hash, verify_password


user_management_router = APIRouter()

@user_management_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.users.User).filter(models.users.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

   
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@user_management_router.post("/add_user/", response_model=dict)
def add_user(
    user: UserSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can add new users.")
    
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    hashed_password = get_password_hash(user.hashed_password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=RoleEnum[user.role] if user.role in RoleEnum.__members__ else RoleEnum.user
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": f"User '{user.username}' added successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")
    
@user_management_router.delete("/delete_user/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.users.User = Depends(get_current_user)):
    # Ensure the current user is an admin
    if current_user.role != models.users.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete users.")
    
    # Find the user to delete
    user_to_delete = db.query(models.users.User).filter(models.users.User.id == user_id).first()
    
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(user_to_delete)
        db.commit()
        return {"message": f"User with ID {user_id} deleted successfully."}
    except Exception as e:
        db.rollback()  # Ensure any failed operation rolls back
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")