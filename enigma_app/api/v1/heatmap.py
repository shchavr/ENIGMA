from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from enigma_app.api.deps import get_current_admin
from enigma_app.db.models.device_problem_heatmap import DeviceProblemHeatmap
from enigma_app.db.session import get_db
from enigma_app.schemas.heatmap import DeviceHeatmapRead

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/heatmap", response_model=List[DeviceHeatmapRead])
def get_device_heatmap(
        db: Session = Depends(get_db),
        admin: dict = Depends(get_current_admin),
):
    """Возвращает тепловую карту проблем по устройствам (только для админов)."""
    heatmap = db.query(DeviceProblemHeatmap).order_by(DeviceProblemHeatmap.problem_count.desc()).all()
    return heatmap
