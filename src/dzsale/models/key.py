#-*- coding: utf-8 -*- 
from openerp import models, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class dzsale_key(models.Model):
		_name="dzsale.key"
		name = fields.Char(string=u"Clé",required=True,readonly=False,size=7)
		company = fields.Char(string=u"Nom de la companie",required=False,readonly=False)
