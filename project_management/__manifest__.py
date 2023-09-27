
{
    'name': 'Projects Management',
    'summary': 'Projects Management',
    'author': "ITSS , Memy Mostafa",
    'company': 'ITSS',
    'version': '15.0.0.1.0',
    'category': 'Rental',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'hr',
        'project',
        'bi_all_in_one_project_management_system',
        'odoo_job_costing_management',
        'property_management_additions',
        'account_accountant',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/project_management.xml',
        'views/investors.xml',
        'views/funding_sources.xml',
        'views/sale_type.xml',
        'views/job_costing.xml',
        'views/investors_verified.xml',
        'views/menu.xml',
        'data/ir_sequence_data.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

