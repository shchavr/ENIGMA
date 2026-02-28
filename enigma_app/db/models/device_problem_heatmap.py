from sqlalchemy import Column, Integer, String

from enigma_app.db import Base


class DeviceProblemHeatmap(Base):
    __tablename__ = "device_problem_heatmap"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_model = Column(String, unique=True, nullable=False)
    problem_count = Column(Integer, default=0)
