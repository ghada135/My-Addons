""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class OfficialPapers(models.Model):
    _name = 'official.papers'
    project_papers_id = fields.Many2one('project.management')
    paper_name = fields.Char('Paper Name')
    paper_description = fields.Html('Paper Description')
    upload = fields.Binary('Upload')

