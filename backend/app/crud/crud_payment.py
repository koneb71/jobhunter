from datetime import datetime
from typing import Any, Dict, List, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentStatus, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.user_id == user_id)
            .order_by(desc(Payment.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: PaymentStatus, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.status == status)
            .order_by(desc(Payment.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_job(
        self, db: Session, *, job_id: str, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.job_id == job_id)
            .order_by(desc(Payment.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: PaymentCreate) -> Payment:
        db_obj = Payment(
            **obj_in.model_dump(),
            transaction_id=f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Payment,
        obj_in: Union[PaymentUpdate, Dict[str, Any]],
    ) -> Payment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if update_data.get("status") == PaymentStatus.COMPLETED:
            update_data["payment_date"] = datetime.now()

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def process_payment(self, db: Session, *, payment_id: str) -> Payment:
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
            "description": "Payment processed successfully",
        }

        return self.update(db, db_obj=payment, obj_in=update_data)


crud_payment = CRUDPayment(Payment)
