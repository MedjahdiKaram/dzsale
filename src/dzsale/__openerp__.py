# -*- coding: utf-8 -*-
##############################################################################
#
#  
##############################################################################
{
	'name': 'Awesome Sales',
	'version': '1.0.0',
	'category': 'Sale',
	'description': """

	Sales log module create by awesomTIC
===============================================================


	""",
	'author': 'AwesomTIC',
	'website': 'https://awesomtic.com',
	'depends': ['base']
	,
	'data' : [	  	  
	  'report/dailysale_report.xml',	  	  	  	  
	  'data/dzsale_sequence.xml',	  	  
	  'views/client_view.xml',	  	  
	  'views/cie_view.xml',	  	  
	  'views/organisation_view.xml',	  	  
	  'views/sale_view.xml',	  	  
	  'views/sline_view.xml',	
	   'views/menuitems.xml'	  	  
	],

	'auto_install': False,
}

