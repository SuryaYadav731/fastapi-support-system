from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return dashboard_service.get_dashboard_stats(db, current_user)


@router.get("/analytics/status")
def status_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return dashboard_service.tickets_by_status(db)


@router.get("/analytics/priority")
def priority_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return dashboard_service.tickets_by_priority(db)


@router.get("/analytics/monthly")
def monthly_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return dashboard_service.monthly_ticket_trend(db)