from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from supabase import Client

from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationStatus

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_by_user(
        self, db: Client, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        response = (
            db.table("notifications")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Notification(**item) for item in response.data]

    def get_unread(
        self, db: Client, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        response = (
            db.table("notifications")
            .select("*")
            .eq("user_id", user_id)
            .eq("status", NotificationStatus.UNREAD)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Notification(**item) for item in response.data]

    def get_by_type(
        self, db: Client, *, user_id: str, notification_type: str, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        response = (
            db.table("notifications")
            .select("*")
            .eq("user_id", user_id)
            .eq("notification_type", notification_type)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Notification(**item) for item in response.data]

    def create(
        self, db: Client, *, obj_in: NotificationCreate
    ) -> Notification:
        db_obj = obj_in.model_dump()
        response = db.table("notifications").insert(db_obj).execute()
        return Notification(**response.data[0])

    def update(
        self,
        db: Client,
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
        
        response = (
            db.table("notifications")
            .update(update_data)
            .eq("id", db_obj.id)
            .execute()
        )
        return Notification(**response.data[0])

    def mark_as_read(
        self, db: Client, *, notification_id: str
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
        self, db: Client, *, user_id: str
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