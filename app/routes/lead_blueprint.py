from flask import Blueprint
from app.controllers.lead_controller import delete_leads, get_leads, create_lead, update_leads

bp_leads = Blueprint("bp_leads", __name__)

bp_leads.post("/leads")(create_lead)
bp_leads.get("/leads")(get_leads)
bp_leads.patch("/leads")(update_leads)
bp_leads.delete("/leads")(delete_leads)
