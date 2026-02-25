from app.db.session import engine
from app.db.base import Base
from app.db.models.user import User
from app.db.models.support_tickets import SupportTicket
from app.db.models.responses import Response
from app.db.models.ml_requests import MLRequest
from app.db.models.emails import Email
from app.db.models.admin_logs import AdminLog

Base.metadata.create_all(bind=engine)
