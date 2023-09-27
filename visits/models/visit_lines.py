from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime, timedelta, time, date


class VisitsLine(models.Model):
    _name = 'visit.lines'
    customer_id = fields.Many2one('res.partner')
    name = fields.Char("Name")
    visit_id = fields.Many2one('visit.visit')
    visit_date = fields.Date("Visit Date", related='visit_id.visit_date')

    def open_visit(self):
        for line in self:
            return {
                'view_mode': 'form,tree',
                'res_model': 'visit.visit',
                'domain': [('id', '=', line.visit_id.id)],
                'res_id': self.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
            }
