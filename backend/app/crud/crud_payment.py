from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from supabase import Client

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentStatus

class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_user(
        self, db: Client, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        response = (
            db.table("payments")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Payment(**item) for item in response.data]

    def get_by_status(
        self, db: Client, *, status: PaymentStatus, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        response = (
            db.table("payments")
            .select("*")
            .eq("status", status)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Payment(**item) for item in response.data]

    def get_by_job(
        self, db: Client, *, job_id: str, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        response = (
            db.table("payments")
            .select("*")
            .eq("job_id", job_id)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Payment(**item) for item in response.data]

    def create(
        self, db: Client, *, obj_in: PaymentCreate
    ) -> Payment:
        db_obj = obj_in.model_dump()
        db_obj["transaction_id"] = f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        response = db.table("payments").insert(db_obj).execute()
        return Payment(**response.data[0])

    def update(
        self,
        db: Client,
        *,
        db_obj: Payment,
        obj_in: Union[PaymentUpdate, Dict[str, Any]]
    ) -> Payment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if update_data.get("status") == PaymentStatus.COMPLETED:
            update_data["payment_date"] = datetime.now()
        
        response = (
            db.table("payments")
            .update(update_data)
            .eq("id", db_obj.id)
            .execute()
        )
        return Payment(**response.data[0])

    def process_payment(self, db: Client, *, payment_id: str) -> Payment:
        """
        Process a payment (simulate payment processing for internal payments)
        """
        payment = self.get(db, id=payment_id)
        if not payment:
            raise ValueError("Payment not found")
        
        if payment.status != PaymentStatus.PENDING:
            raise ValueError("Payment is not in pending status")
        
        # Simulate payment processing
        update_data = {
            "status": PaymentStatus.COMPLETED,
            "payment_date": datetime.now(),
            "description": "Payment processed successfully"
        }
        
        return self.update(db, db_obj=payment, obj_in=update_data)

crud_payment = CRUDPayment(Payment) 