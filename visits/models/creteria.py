from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime, timedelta, time, date




class Criteria(models.Model):
    _name = 'criteria.criteria'

    visit = fields.Char()
    criteria = fields.Char()
    intervension = fields.Char()
    visit_id = fields.Many2one('visit.visit')



