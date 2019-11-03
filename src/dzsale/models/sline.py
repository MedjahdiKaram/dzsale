#-*- coding: utf-8 -*- 
from openerp import models, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.exceptions import ValidationError

class dzsale_sline(models.Model):
	
		_name="dzsale.sline"
		
		
		name = fields.Char(string=u"Ligne de vente",required=False,readonly=True,compute='_compute_name',store=True) 
		ticket = fields.Char(string=u"Billet",required=False,readonly=False)
		transaction_type = fields.Selection(string=u"Transaction",selection=[('payment', 'Payement'),('collection', 'Encaissement'),('refund', 'Remboursement')],default='payment',required=True,readonly=False)
		payment_type = fields.Selection(string=u"Payement",selection=[('checkout', 'Caisse'),('bank', u'Chèque'),('inaccount', 'E/C')],required=True,readonly=False)
		invoice_num = fields.Char(string=u"N° de facture",required=False,readonly=False)
		amount = fields.Float(string=u"Montant",required=True,readonly=False)
		price = fields.Float(string=u"Prix",required=False,readonly=False)
		cie = fields.Many2one("dzsale.cie",string=u"CIE",required=False,readonly=False)
		client = fields.Many2one("dzsale.client",string=u"Client",required=True,readonly=False)
		organisation = fields.Many2one("dzsale.organisation",string=u"Organisme",required=False,readonly=False)
		sale = fields.Many2one("dzsale.sale",string=u"Vente",required=False,readonly=False)
		cheque = fields.Char(string=u"Chèque",required=False,readonly=False)	
		@api.onchange('price')
		def _onchange_price(self):
			self.amount=self.price
				
		@api.one
		@api.depends('ticket','cie')
		def _compute_name(self):
			if self.cie:
				if self.ticket:
					self.name= self.cie.name+ self.ticket 
		@api.one
		@api.constrains('transaction_type', 'payment_type','price','amount','cheque','invoice_num')
		def _check_sline(self):
			if (self.transaction_type == 'collection' and self.payment_type=='inaccount') or (self.transaction_type == 'refund' and self.payment_type=='bank'):
				raise ValidationError(u"Le type de transaction est incompatyble avec le mode de payement sélectionné")
			if self.payment_type=='bank' and self.cheque==False:
				raise ValidationError(u"Le champs 'Chèque' ne peut être vide.")
			if (self.invoice_num==False and (self.payment_type=='inacount' and self.transaction_type=='payment') or (self.amount<self.price)):
				raise ValidationError(u"Le champs 'N° de facture ne peut être vide' ne peut être vide.")