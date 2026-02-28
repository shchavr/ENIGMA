from pydantic import BaseModel


class DeviceHeatmapRead(BaseModel):
    device_model: str
    problem_count: int

    class Config:
        from_attributes = True
