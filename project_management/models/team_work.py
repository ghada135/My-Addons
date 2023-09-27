""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class TeamWork(models.Model):
    _name = 'team.work'
    project_management_id = fields.Many2one('project.management')
    employee_id = fields.Many2one('hr.employee')
    job_id = fields.Many2one('hr.job',related='employee_id.job_id')



