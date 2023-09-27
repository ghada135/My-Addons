{
    'name': 'Crm Edits',
    'summary': """ 
    1. Add some information at CRM 
    2. Partner restriction ( vendor bill - invoice - Refund - Credit note - Po - So - CRM ) 
    3. add a new field called is employee in res.partner
    """,
    'author': "ITSS , Memy",
    'company': 'ITSS',
    'website': "https://www.itss-c.com",
    'version': '16.0.0.1.0',
    'category': 'Crm',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'crm',
        'sale',
        'account',
        'purchase',
        'sale_crm',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sigmentation_type.xml',
        'views/client_type.xml',
        'views/industry_type.xml',
        'views/lead_type.xml',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_lead_oppo_partner_views.xml',
        'views/probability_percentage.xml',
        'views/probability_state.xml',
        'views/crm_team_views.xml',
        'views/sale_order.xml',
        'data/ir_sequence_data.xml',

    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
