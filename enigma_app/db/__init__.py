from enigma_app.db.session import engine
from enigma_app.db.base import Base
from enigma_app.db.models.user import User
from enigma_app.db.models.support_tickets import SupportTicket
from enigma_app.db.models.responses import Response
from enigma_app.db.models.ml_requests import MLRequest
from enigma_app.db.models.emails import Email
from enigma_app.db.models.admin_logs import AdminLog

Base.metadata.create_all(bind=engine)
