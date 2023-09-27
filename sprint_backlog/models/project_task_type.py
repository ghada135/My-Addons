from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    sprint_status_to_do = fields.Boolean('Sprint Status - To Do')
    sprint_status_pending = fields.Boolean( 'Sprint Status - Pending' )
    sprint_status_done = fields.Boolean('Sprint Status - Done')

    @api.constrains('sprint_status_to_do', 'sprint_status_pending','sprint_status_done')
    def _stage_changing(self):
        for rec in self:
            if rec.sprint_status_to_do == True and rec.sprint_status_pending == True:
                raise ValidationError('Two Sprint Status Selected True')
            if rec.sprint_status_to_do == True and rec.sprint_status_done == True:
                raise ValidationError('Two Sprint Status Selected True')
            if rec.sprint_status_done == True and rec.sprint_status_pending == True:
                raise ValidationError('Two Sprint Status Selected True')




