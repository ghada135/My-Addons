from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class ProjectType(models.Model):
    _name = "project.type"
    _rec_name = 'type_name'

    project_id = fields.Many2one('project.management')
    type_id = fields.Many2one('unit.type')
    type_ids = fields.Many2many('unit.type',related='project_id.project_product_type_ids')
    type_name = fields.Char(
        related='type_id.name')

    unit_number = fields.Integer('Unit Number')
    area = fields.Integer('Area')
    floor_number_id = fields.Many2one('floor.number')
    setting_rooms_number = fields.Integer('Setting Rooms')
    bed_rooms_number = fields.Integer('Ded Rooms')
    bath_rooms = fields.Integer('Bath Rooms')
    kitchens = fields.Integer('Kitchens')
    halls = fields.Integer('Hall Numbers')
    sale_type_id = fields.Many2one(
        'sale.type', string='Sale Type')


    


