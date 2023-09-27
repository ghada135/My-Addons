""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class JobCosting(models.Model):
    _inherit = 'job.costing'
    # project_id = fields.Many2one('project.management')
    project_management_id = fields.Many2one('project.management')
    partner_id = fields.Many2one('res.partner',required=0)


