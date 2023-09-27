{
    'name': 'Visits History',
    'summary': 'visits Addition For Customers',
    'author': "ITSS , Memy Mostafa",
    'company': 'ITSS',
    'website': "http://www.itss-c.com",
    'version': '16.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account_accountant',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/visits_view.xml',
        'views/partner_view.xml',
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
