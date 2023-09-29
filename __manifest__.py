{
    'name': "Upaya",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail', 'logic_base', 'portal', 'web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rule_upaya.xml',
        'views/upaya.xml',
        'data/activity.xml',
        'views/upaya_teams.xml'

    ],
    'assets': {
        'web.assets_backend': [
            'upaya/static/src/css/winning_effect.css'],
    },

    'demo': [],
    'summary': "upaya_logic",
    'description': "this_is_upaya_module",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
