from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class ProjectManagement(models.Model):
    _name = "project.management"
    _rec_name = 'project_name'

    project_name = fields.Char()
    project_reference = fields.Char(string='Reference', readonly=True)
    land_size = fields.Float('Land Size')
    land_area = fields.Float('Land Area')
    expected_cost = fields.Float('expected Cost')
    actual_cost = fields.Float('Actual Cost')
    start_date = fields.Date('Project Start Date')
    end_date = fields.Date('Project End Date')

    # address
    street = fields.Char('Street', readonly=False, store=True)
    street2 = fields.Char('Street2', readonly=False, store=True)
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True)
    city = fields.Char('City', readonly=False, store=True)
    state_id = fields.Many2one(
        "res.country.state", string='State', readonly=False, store=True,
        domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one(
        'res.country', string='Country', readonly=False, store=True)
    township = fields.Char(
        string='Township')

    funding_sources_ids = fields.Many2many(
        'funding.source', string='Funding Source')
    project_engineer_id = fields.Many2one(
        'res.users', string='Project Engineer')
    consultation_office = fields.Many2one(
        'res.partner', string='Consultation Office')

    project_project_id = fields.Many2one('project.project', string='Project Project ')
    property_id = fields.Many2one('account.asset', string='Project Manager')
    project_manager_id = fields.Many2one('res.users', string='Project Manager')
    type_id = fields.Many2one(comodel_name='property.type', string="Project Type")
    project_product_type_ids = fields.Many2many(comodel_name='unit.type', string="Project Product Types")
    project_type_ids = fields.One2many(comodel_name='project.type', inverse_name='project_id')
    responsibles_ids = fields.One2many(comodel_name='responsibles', inverse_name='project_responsibles_id')
    team_ids = fields.Many2many(comodel_name='team.work', inverse_name='project_management_id')
    official_papers_ids = fields.One2many(comodel_name='official.papers', inverse_name='project_papers_id')
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account')
    state = fields.Selection([('new', 'New'),
                              ('under_studying', 'Under Studying'),
                              ('waiting_for_internal_approval', 'Waiting For Internal Approval'),
                              ('waiting_for_external_approval', 'Waiting For External Approval'),
                              ('start_implementation', 'Start Implementation'),
                              ('implemented', 'Implemented'),
                              ('delivery_of_units', 'Delivery Of Units'),
                              ],
                             default='new')

    def compute_has_group(self):
        if self.env.user.has_group('project_management.group_under_studying') or self.env.user.has_group(
                'project_management.group_internal_approval') or self.env.user.has_group(
            'project_management.group_external_approval') or self.env.user.has_group(
            'project_management.group_implementation') or self.env.user.has_group(
            'project_management.group_implemented') or self.env.user.has_group(
            'project_management.group_delivary'):
            print('ghhhhhh')
            self.has_group = True
        else:
            print('iouytrew')
            self.has_group = False

    # Boolean Fields

    job_cost_created = fields.Boolean()
    unit_created = fields.Boolean()
    has_group = fields.Boolean(compute='compute_has_group')

    @api.model
    def create(self, vals):
        res = super(ProjectManagement, self).create(vals)
        if not res.project_reference or res.project_reference == _('New'):
            res.project_reference = self.env['ir.sequence'].next_by_code('project.management') or _('New')
        if res.project_name:
            analytic = self.env['account.analytic.account'].create({
                'name': res.project_name,
                'code': res.project_reference,
            })
            res.analytic_account_id = analytic
            project = self.env['project.project'].create({
                'name': res.project_name,
            })
            res.project_project_id = project

            asset = self.env['account.asset'].create({
                'name': res.project_name,
                'classification': 'proper',
                'type_id': res.type_id.id,
                'property_manager': res.consultation_office.id,
                'city': res.city,
                'state_id': res.state_id.id,
                'street': res.street,
                'street2': res.street2,
                'township': res.township,
                'zip': res.zip,
            })
            res.property_id = asset
        return res

    def create_units(self):
        if not self.project_type_ids:
            raise ValidationError("First Select Project Products")
        for line in self.project_type_ids:
            print('ghada', line.type_name)
            asset = self.env['account.asset'].create({
                'classification': 'unit',
                'name': line.type_name,
                'unit_name': line.type_name,
                'unit_type_id': line.type_id.id,
                'type_id': line.project_id.type_id.id,
                'parent_id': line.project_id.property_id.id,
                'floor_number_id': line.floor_number_id.id,
                'property_manager': line.project_id.consultation_office.id
            })
        self.unit_created = True

    def under_studying(self):
        for rec in self:
            rec.state = 'under_studying'

    def internal_approval(self):
        for rec in self:
            rec.state = 'waiting_for_internal_approval'

    def external_approval(self):
        for rec in self:
            rec.state = 'waiting_for_external_approval'

    def implementation(self):
        for rec in self:
            rec.state = 'start_implementation'

    def implemented(self):
        for rec in self:
            rec.state = 'implemented'

    def delivary(self):
        for rec in self:
            rec.state = 'delivery_of_units'

    def action_job_cost(self):
        for rec in self:
            job_cost = self.env['job.costing'].create({
                'name': rec.project_name,
                'project_management_id': rec.id,
                'project_id': rec.project_project_id.id,
                'analytic_id': rec.analytic_account_id.id,
            })
            rec.job_cost_created = True

    def open_job_cost(self):
        job_cost = self.env['job.costing'].search([('project_management_id', '=', self.id)])
        return {
            'name': 'Job Cost Sheet',
            'type': 'ir.actions.act_window',
            'res_model': 'job.costing',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', job_cost.ids)],
            'target': 'current',
        }

    def open_units(self):
        units = self.env['account.asset'].search([('parent_id', '=', self.property_id.id),
                                                  ('classification', '=', 'unit')])
        return {
            'name': 'Units For %s ' % (self.project_name),
            'type': 'ir.actions.act_window',
            'res_model': 'account.asset',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', units.ids)],
            'target': 'current',
        }
