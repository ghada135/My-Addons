from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime, timedelta, time, date



class Comparison(models.Model):
    _name = 'illness.comparison'
    illness_name = fields.Char("Illness Name")
    before_surgery = fields.Text('Before Surgery')
    after_surgery = fields.Text('After Surgery')
    visit_id = fields.Many2one('visit.visit')

