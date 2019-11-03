#-*- coding: utf-8 -*- 
from openerp import models, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class dzsale_client(models.Model):
		_name="dzsale.client"
		name = fields.Char(string=u"Nom complet",required=True,readonly=False)
		sex = fields.Selection(string=u"Sexe",selection=[('m', 'Homme'),('w', 'Femme')],default='m',required=True,readonly=False)
		dob = fields.Date(string=u"Date de naissance",required=False,readonly=False)		
		mob = fields.Char(string=u"Mobile",required=False,readonly=False)
		passsport_id = fields.Char(string=u"Numéro de passport",required=False,readonly=False)
		passsport_delivery = fields.Date(string=u"Déliverance du passport",required=False,readonly=False)
		passsport_expiry = fields.Date(string=u"Expiration du passport",required=False,readonly=False)
		adress = fields.Char(string=u"Adresse",size=128,required=False,readonly=False)
		debt = fields.Float(string=u"Dette",required=False,readonly=True)