from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client

from app.core.deps import get_db
from app.core.security import get_current_active_user
from app.crud import crud_notification
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate, NotificationResponse, NotificationUpdate,
    NotificationType, NotificationStatus
)

router = APIRouter()

@router.get("/my-notifications", response_model=List[NotificationResponse])
def get_my_notifications(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get current user's notifications.
    """
    return crud_notification.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/unread", response_model=List[NotificationResponse])
def get_unread_notifications(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get current user's unread notifications.
    """
    return crud_notification.get_unread(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/type/{notification_type}", response_model=List[NotificationResponse])
def get_notifications_by_type(
    notification_type: NotificationType,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get current user's notifications by type.
    """
    return crud_notification.get_by_type(
        db, user_id=current_user.id, notification_type=notification_type, skip=skip, limit=limit
    )

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific notification by id.
    """
    notification = crud_notification.get(db, id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )
    if not current_user.is_superuser and notification.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return notification

@router.post("/", response_model=NotificationResponse)
def create_notification(
    *,
    db: Client = Depends(get_db),
    notification_in: NotificationCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new notification (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_notification.create(db, obj_in=notification_in)

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    *,
    db: Client = Depends(get_db),
    notification_id: str,
    notification_in: NotificationUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a notification.
    """
    notification = crud_notification.get(db, id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )
    if not current_user.is_superuser and notification.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_notification.update(db, db_obj=notification, obj_in=notification_in)

@router.post("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(
    *,
    db: Client = Depends(get_db),
    notification_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Mark a notification as read.
    """
    notification = crud_notification.get(db, id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )
    if not current_user.is_superuser and notification.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    try:
        return crud_notification.mark_as_read(db, notification_id=notification_id)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/read-all", response_model=List[NotificationResponse])
def mark_all_notifications_as_read(
    *,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Mark all user's notifications as read.
    """
    return crud_notification.mark_all_as_read(db, user_id=current_user.id) 