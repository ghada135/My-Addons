from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class Type(models.Model):
    _name = "type.type"
    _rec_name='name'

    name = fields.Char("Name",required=1)



    


