from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class Pesponsibles(models.Model):
    _name = "responsibles"
    project_responsibles_id = fields.Many2one('project.management')
    user_id = fields.Many2one('hr.employee')
    phone = fields.Char("Phone",related='user_id.phone')
    email = fields.Char("Email")
    notes = fields.Html("Notes")
    job_id = fields.Many2one('hr.job',related='user_id.job_id')


    


