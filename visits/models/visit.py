from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime, timedelta, time, date


class Visits(models.Model):
    _name = "visit.visit"
    _rec_name = 'visit_reference'

    visit_reference = fields.Char(string='Reference', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    age = fields.Integer("Age")
    work = fields.Char("Work")
    visit_date = fields.Date("Visit Date")
    comparison_ids = fields.One2many(comodel_name='illness.comparison', inverse_name='visit_id')
    criteria_ids = fields.One2many(comodel_name='criteria.criteria', inverse_name='visit_id')
    cups = fields.Char(default='CUPS')
    kg = fields.Char(default='KG')
    cm = fields.Char(default='Cm')

    martial_state = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorce', 'Divorce')],
        required=True, default='single', string="Martial State")

    allergy = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="Allergy")
    financials = fields.Selection([
        ('law', 'Law'),
        ('moderate', 'Moderate'),
        ('high', 'High')],
        required=True, default='law', string="Financials")
    food_craving = fields.Selection([
        ('sweet', 'Sweet'),
        ('bulky', 'Bulky'),
        ('pepsi', 'Pepsi'),
        ('chronic_dieter', 'Chronic Dieter'),
        ('non_approval_FDA_medication', 'Non Approval FDA Medication'),
        ('approval_medication ', 'Approval Medication ')],
        required=True, default='sweet', string="Type of food craving")
    type_of_wls = fields.Selection([
        ('sleeve', 'Sleeve'),
        ('mgb', 'MGB'),
        ('sas_J', 'Sas _J'),
        ('Roux_en_y_gastric by pass', 'Roux _ en _ y _ gastric by pass'),
        ('capsule', 'Capsule'),
        ('ballon', 'Ballon')],
        required=True, default='sleeve', string="Type of food craving")

    contraceptive_method = fields.Selection([
        ('iud', 'IUD'),
        ('implant', 'Implant'),
        ('pills', 'Pills'),
        ('monthly_injection', 'Monthly injection'),
        ('3_month_injection', '3 Month Injection'),
        ('condom', 'Condom'),
        ('no_method', 'No Method'),
    ],
        required=True, default='no_method', string="Contraceptive method")

    duration_type = fields.Selection([
        ('month', 'Month'),
        ('year', 'Year')],
        required=True, default='month', string="Type")

    hours_sleep = fields.Selection([
        ('regular', 'Regular'),
        ('irregular', 'IR Regular')],
        required=True, default='regular', string="Hours Of Sleep")
    diabetes = fields.Selection([
        ('type1', 'Type1'),
        ('type2', 'Type2')],
        required=True, default='type1', string="Diabetes")
    diabetes_duraton = fields.Integer('Duration')
    diabetes_medication = fields.Selection([
        ('insulin', 'Insulin'),
        ('oral_hypo-glycemic_agent', 'Oral Hypo-Glycemic Agent')],
        required=True, default='insulin', string="Medication")

    htn = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="HTN")
    htn_duraton = fields.Integer('Duration')
    htn_medication = fields.Selection([
        ('single_therapy', 'Single Therapy'),
        ('double_therapy', 'Double Therapy'),
        ('triple_therapy', 'Triple Therapy')],
        required=True, default='single_therapy', string="Medication")

    dyslipidemia = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="Dyslipidemia")
    sleep_apnea = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="Sleep Apnea")
    reflux = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="Reflux")
    gall_bladder_disease = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="Gall Bladder Disease")

    thyroid_dysfunction = fields.Selection([
        ('hypo', 'Hyper'),
        ('hyper', 'Hyper')],
        required=True, default='hypo', string="Thyroid Dysfunction")
    medications_Eltroxin = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        required=True, default='yes', string="Medications (Eltroxin)")
    dose = fields.Selection([
        ('50', '50'),
        ('100', '100'),
        ('150', '150'),
        ('200', '200'),
        ('250', '250'),
        ('300', '300')],
        required=True, default='50', string="Dose")
    weight = fields.Char("")
    height = fields.Char("")
    muscle_mass = fields.Char("")
    fat_mass = fields.Char("")
    water = fields.Integer("")
    hydration = fields.Char("")

    exercises = fields.Selection([
        ('No', 'NO Exercises'),
        ('walking', 'Walking'),
        ('gym', 'GYM')],
        required=True, default='No', string="Exercises")

    nausea = fields.Boolean()
    vomiting = fields.Boolean()
    diarrhea = fields.Boolean()
    burping = fields.Boolean()
    de_hydration = fields.Boolean()
    constipation = fields.Boolean()
    low_protein_intake = fields.Boolean()
    low_food_intake = fields.Boolean()
    bad_adherence = fields.Boolean()
    hair_loss = fields.Boolean()

    multivitamins = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Multivitamins")
    hair_supplementation = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Hair Supplementation")

    iron = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Iron")
    ca = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="CA")
    Vit_D = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Vit D")
    folic_acid = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Folic Acid ")

    vit_b12 = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Vit B12")

    protein = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="Protein")
    ppis = fields.Selection([
        ('mild_adherence', 'Mild Adherence'),
        ('moderate_adherence', 'Moderate Adherence'),
        ('bad_adherence', 'Bad Adherence')],
        required=True, default='mild_adherence', string="PPIS")


    @api.model
    def create(self, vals):
        res = super(Visits, self).create(vals)
        if not res.visit_reference or res.visit_reference == _('New'):
            res.visit_reference = self.env['ir.sequence'].next_by_code('visit.visit') or _('New')
        print(res)

        if res.customer_id:
            visits = self.env['visit.lines'].create({
                'customer_id': res.customer_id.id,
                'name': res.visit_reference,
                'visit_id': res.id,
            })
        return res
