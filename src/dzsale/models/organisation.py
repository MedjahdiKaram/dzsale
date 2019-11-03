#-*- coding: utf-8 -*- 
from openerp import models, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class dzsale_organisation(models.Model):
		_name="dzsale.organisation"
		name = fields.Char(string=u"Nom de l'organisme",required=True,readonly=False)
		fiscal_num = fields.Char(string=u"Numero fiscal",required=False,readonly=False)
		debt = fields.Float(string=u"Dette",required=False,readonly=True)
		phone = fields.Char(string=u"Telephone",required=False,readonly=False)