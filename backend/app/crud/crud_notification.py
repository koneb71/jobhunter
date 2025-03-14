from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationStatus

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(desc(Notification.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_unread(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .filter(Notification.status == NotificationStatus.UNREAD)
            .order_by(desc(Notification.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type(
        self, db: Session, *, user_id: str, notification_type: str, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .filter(Notification.notification_type == notification_type)
            .order_by(desc(Notification.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self, db: Session, *, obj_in: NotificationCreate
    ) -> Notification:
        db_obj = Notification(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Notification,
        obj_in: Union[NotificationUpdate, Dict[str, Any]]
    ) -> Notification:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if update_data.get("status") == NotificationStatus.READ:
            update_data["read_at"] = datetime.now()
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def mark_as_read(
        self, db: Session, *, notification_id: str
    ) -> Notification:
        """
        Mark a notification as read
        """
        notification = self.get(db, id=notification_id)
        if not notification:
            raise ValueError("Notification not found")
        
        if notification.status == NotificationStatus.READ:
            raise ValueError("Notification is already read")
        
        update_data = {
            "status": NotificationStatus.READ,
            "read_at": datetime.now()
        }
        
        return self.update(db, db_obj=notification, obj_in=update_data)

    def mark_all_as_read(
        self, db: Session, *, user_id: str
    ) -> List[Notification]:
        """
        Mark all user's notifications as read
        """
        notifications = self.get_by_user(db, user_id=user_id)
        updated_notifications = []
        
        for notification in notifications:
            if notification.status == NotificationStatus.UNREAD:
                update_data = {
                    "status": NotificationStatus.READ,
                    "read_at": datetime.now()
                }
                updated_notifications.append(
                    self.update(db, db_obj=notification, obj_in=update_data)
                )
        
        return updated_notifications

crud_notification = CRUDNotification(Notification) 