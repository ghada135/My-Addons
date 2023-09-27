# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError



class CloseSprint(models.TransientModel):
    _name = 'close.sprint'
    sprint_name_id = fields.Many2one('sprint.backlog', "Sprint Backlog", required=1)

    """ Method used to close Sprint """
    def close_sprint(self):
        self.sprint_name_id.state = 'closed'


    """ Method used to call wizard that 
    from you can select another sprint """

    def migrate_yes(self):
        return {
            'name': ('Select Sprint'),
            'view_mode': 'form',
            'res_model': 'select.sprint',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_type': 'from_task',
                'default_sprint_name_id': self.sprint_name_id.id
            }, }


class SelectSprint(models.TransientModel):
    _name = 'select.sprint'
    is_bug = fields.Boolean()
    sprint_id = fields.Many2one('sprint.backlog', "Sprint Backlog",
                                required=0)
    sprint_name_id = fields.Many2one('sprint.backlog', "Sprint Backlog")
    backlog_sprint_line_id = fields.Many2one('sprint.backlog.line')
    backlog_sprint_bug_id = fields.Many2one('sprint.backlog.bugs')

    type = fields.Selection([
        ('from_task', 'From Task'),
        ('from_line', 'From Line')],
        required=True, default='from_line')

    """ Method used to put tasks into the Sprint you select """
    def migrate_yes(self):
        pro = []
        if self.is_bug == False:
            if self.sprint_id:
                if self.type == 'from_task':
                    tasks = self.env['sprint.backlog.line'].search([('backlog_sprint_id', '=', self.sprint_name_id.id),
                                                                    ('status', '!=', 'done')])
                    if tasks:
                        for task in tasks:
                            print(task.task_id.name)
                            vals = {
                                'backlog_sprint_id': self.sprint_id.id,
                                'task_id': task.task_id.id,
                                'project_id': task.project_id.id,
                                'developer_id': task.developer_id.id,
                                'hours': task.hours,
                                'notes': task.notes,
                                'migration': 'migrated',
                                'task_weight': task.task_weight,
                                'status': task.status, }
                            pro.append((0, 0, vals))
                else:
                    vals = {
                        'backlog_sprint_id': self.sprint_id.id,
                        'task_id': self.backlog_sprint_line_id.task_id.id,
                        'project_id': self.backlog_sprint_line_id.project_id.id,
                        'developer_id': self.backlog_sprint_line_id.developer_id.id,
                        'hours': self.backlog_sprint_line_id.hours,
                        'notes': self.backlog_sprint_line_id.notes,
                        'migration': 'migrated',
                        'task_weight': self.backlog_sprint_line_id.task_weight,
                        'status': self.backlog_sprint_line_id.status, }
                    pro.append((0, 0, vals))
                self.sprint_id.backlog_sprint_ids = pro
            else:
                raise ValidationError("Selec Sprint Please!")
        else:
            if self.sprint_id:
                vals = {
                    'backlog_sprint_id': self.sprint_id.id,
                    'task_id': self.backlog_sprint_bug_id.task_id.id,
                    'project_id': self.backlog_sprint_bug_id.project_id.id,
                    'developer_id': self.backlog_sprint_bug_id.developer_id.id,
                    'hours': self.backlog_sprint_bug_id.hours,
                    'notes': self.backlog_sprint_bug_id.notes,
                    'migration': 'migrated',
                    'task_weight': self.backlog_sprint_bug_id.task_weight,
                    'status': self.backlog_sprint_bug_id.status, }
                pro.append((0, 0, vals))
                self.sprint_id.backlog_sprint_bugs_ids = pro
            else:
                raise ValidationError("Selec Sprint Please!")

    """ Method used to close Sprint """
    def close_sprint(self):
        self.sprint_name_id.state = 'closed'
