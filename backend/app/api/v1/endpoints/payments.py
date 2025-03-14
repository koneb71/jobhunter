from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client

from app.core.deps import get_db
from app.core.security import get_current_active_user
from app.crud import crud_payment
from app.models.user import User
from app.schemas.payment import (
    PaymentCreate, PaymentResponse, PaymentUpdate,
    PaymentStatus, PaymentType
)

router = APIRouter()

@router.get("/my-payments", response_model=List[PaymentResponse])
def get_my_payments(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get current user's payments.
    """
    return crud_payment.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/status/{status}", response_model=List[PaymentResponse])
def get_payments_by_status(
    status: PaymentStatus,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get payments by status (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_payment.get_by_status(db, status=status, skip=skip, limit=limit)

@router.get("/job/{job_id}", response_model=List[PaymentResponse])
def get_job_payments(
    job_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get payments for a specific job (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_payment.get_by_job(db, job_id=job_id, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific payment by id.
    """
    payment = crud_payment.get(db, id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )
    if not current_user.is_superuser and payment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return payment

@router.post("/", response_model=PaymentResponse)
def create_payment(
    *,
    db: Client = Depends(get_db),
    payment_in: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new payment.
    """
    if not current_user.is_superuser and payment_in.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_payment.create(db, obj_in=payment_in)

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    *,
    db: Client = Depends(get_db),
    payment_id: str,
    payment_in: PaymentUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a payment (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    payment = crud_payment.get(db, id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )
    return crud_payment.update(db, db_obj=payment, obj_in=payment_in)

@router.post("/{payment_id}/process", response_model=PaymentResponse)
def process_payment(
    *,
    db: Client = Depends(get_db),
    payment_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Process a payment (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    try:
        return crud_payment.process_payment(db, payment_id=payment_id)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) 