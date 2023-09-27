from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime, timedelta, time, date


class Partner(models.Model):
    _inherit = "res.partner"
    visit_ids = fields.One2many('visit.lines', 'customer_id')




