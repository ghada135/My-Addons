from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.onchange('partner_id')
    def onchange_product_list(self):
        for rec in self:
            if rec.type == "opportunity":
                return {'domain': {'partner_id': [('is_employee', '=', False), ('customer_rank', '>', 0)]}}

    reference = fields.Char("Lead/Oppo NO", readonly=False, copy=False)
    appraisals_id = fields.Many2one('res.users', required=False, string='Pre_sales Name')
    appraisals_ids = fields.Many2many('res.users', 'crm_appraisals_ids',
                                      compute='compute_manager_and_appraisals'
                                      )
    account_manager_id = fields.Many2one('res.users', required=False)
    account_manager_ids = fields.Many2many('res.users', 'crm_account_manager_ids',
                                           compute='compute_manager_and_appraisals'
                                           )
    partner_lead = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True,
        default='yes', string="Are We Prime")

    poc = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=False,
        default='', string="POC")
    existing_market_place = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=False,
        default='', string="Existing Matket Place")


    partner_name_new = fields.Char("In House Product Value")
    partner_value = fields.Char("Non-In House Product Value")
    partner_vendor = fields.Char(string="Vendor Name")
    partner_list_id = fields.Many2many('res.partner', domain="[('is_employee', '=', False)]", )
    contract_duration = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),

    ], string='Contract Duration', )
    contract_state = fields.Selection([
        ('month', 'Month'),
        ('year', 'Year'),
    ], string='Contract State', )



    @api.depends('team_id')
    def compute_manager_and_appraisals(self):
        for rec in self:
            manager_and_appraisals = self.env['crm.team'].search([('id', '=', self.team_id.id)])
            if manager_and_appraisals.appraisals_ids:
                if manager_and_appraisals.appraisals_ids:
                    rec.appraisals_ids = manager_and_appraisals.appraisals_ids.ids
                if manager_and_appraisals.account_manager_ids:
                    rec.account_manager_ids = manager_and_appraisals.account_manager_ids
            else:
                rec.appraisals_ids = False
                rec.account_manager_ids = False

    prop_percentage_id = fields.Many2one('prop.percentage', store=True, string="Probability")
    prop_percentage_status = fields.Char("Probability Status",
                                         related='prop_percentage_id.prob_State_id.prob_State_name'
                                         )
    client_name = fields.Char(
        related='partner_id.client_type_id.client_name', store=True
    )
    sigment_name = fields.Char(
        related='partner_id.sigmentation_type_id.sigment_name', store=True
    )
    industry_name = fields.Char(
        related='partner_id.industry_type_id.industry_name', store=True
    )
    lead_id = fields.Many2one(
        'lead.type', string="Lead / Opp Type"
    )
    is_government = fields.Boolean(related='partner_id.client_type_id.is_government', store=True)
    government_cr = fields.Char("Government CR", related='partner_id.government_cr', store=True)

    def unlink(self):
        if self.env.user.has_group('crm_edits.group_crm_delete_responsible'):
            return super(CrmLead, self).unlink()
        else:
            raise ValidationError("You ARE Not Allowed To Delete")

    expected_revenue = fields.Monetary('Total Contract Value', currency_field='company_currency',
                                       tracking=True)
    company_currency = fields.Many2one("res.currency", string='Currency', compute="_compute_company_currency",
                                       compute_sudo=True)

    @api.depends('company_id')
    def _compute_company_currency(self):
        for lead in self:
            if not lead.company_id:
                lead.company_currency = self.env.company.currency_id
            else:
                lead.company_currency = lead.company_id.currency_id

    # @api.model
    # def create(self, vals):
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code(
    #             'oppo.lead.sequence') or _('New')
    #     if vals['expected_revenue'] <= 0:
    #         raise ValidationError("Total Contract Value Must Not Be 0")
    #     res = super(CrmLead, self).create(vals)
    #     return res
    #
    # def write(self, vals):
    #     res = super(CrmLead, self).write(vals)
    #     for rec in self:
    #         if rec.expected_revenue <= 0:
    #             raise ValidationError("Total Contract Value Must Not Be 0")
    #         else:
    #             pass
    #     return res

    def action_new_quotation(self):
        print("allah")
        action = super(CrmLead, self).action_new_quotation()
        action['context']['default_reference'] = self.reference
        print(action)
        return action
