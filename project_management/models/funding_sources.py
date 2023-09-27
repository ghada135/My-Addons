from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class FundingSource(models.Model):
    _name = "funding.source"
    _rec_name = 'funding_name'

    funding_name = fields.Char("Funding Name")
