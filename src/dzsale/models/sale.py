#-*- coding: utf-8 -*- 
from openerp import models, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class dzsale_sale(models.Model):
		def _get_date(self):
			return datetime.now();
		
			
		_name="dzsale.sale"
		name = fields.Char(string=u"Nom",required=False,readonly=True,compute="_get_name")
		_sql_constraints = [('unique_state', 'unique(date)', 'Une session existe avec cette même date !')]
		date = fields.Date(string=u"Date",required=True,readonly=False,default=_get_date)
		
		total_payment_checkout = fields.Float(string=u"Ventes en caisse",readonly=True,compute="_get_total_payment_checkout",store=True,default=0.0)
		total_payment_bank = fields.Float(string=u"Ventes par chèque",required=False,readonly=True,store=True,compute="_get_total_payment_bank",default=0.0)
		total_payment_inaccount = fields.Float(string=u"Ventes en compte",readonly=True,compute="_get_total_payment_inaccount",store=True,default=0.0)

		total_refund_checkout = fields.Float(string=u"Remboursements liquide",readonly=True,compute="_get_total_refund_checkout",store=True,default=0.0)
		total_refund_inaccount = fields.Float(string=u"Total des avoirs",readonly=True,compute="_get_total_refund_inaccount",store=True,default=0.0)

		total_dept_checkout=fields.Float(string=u"Dettes payés en liquide",compute="_get_total_dept_checkout",readonly=True,store=True,default=0.0)
		total_debt_bank=fields.Float(string=u"Dettes payés en chèque",store=True,readonly=True,compute="_get_total_debt_bank",default=0.0)
		
		total_dept = fields.Float(string=u"Total des dettes encaissées",store=True,readonly=True,compute="_get_total_dept",help=u"Total des règlements de dettes en Liquide et en chèque",default=0.0)
		total_payment = fields.Float(string=u"Total des payements",store=True,readonly=True,compute="_get_total_payment",help="Total des payements (Liquide, chèque et en E/C)",default=0.0)
		total_refund = fields.Float(string=u"Total des remboursements",store=True,readonly=True,compute="_get_total_refund",help=u"Somme des remboursements liquides et avoirs",default=0.0)
		total_checkout = fields.Float(string=u"Total en caisse",store=True,readonly=True,compute="_get_total_checkout", help=u"Somme des ventes en liquide (ventes et règlement de dettes)",default=0.0)

		slines = fields.One2many("dzsale.sline","sale",string=u"Ventes",required=False,readonly=False)
		state = fields.Selection(string=u"Etat",selection=[('draft', 'Brouillon'),('open', 'Ouvert'),('close', u'Fermé')],default='draft',required=True,readonly=True)



		@api.one
		def _get_name(self):
			if self.id:
				 self.name="S"+str(self.id)
		
		@api.one
		@api.depends("slines")
		def _get_total_payment_checkout(self):
			if self.slines:
				self.total_payment_checkout=sum(e.amount for e in self.slines if e.payment_type=='checkout' and  e.transaction_type=='payment')
		
		@api.one
		@api.depends("slines")
		def _get_total_payment_bank(self):
			if self.slines:
				self.total_payment_bank=sum(e.amount for e in self.slines if e.payment_type=='bank' and  e.transaction_type=='payment')

		@api.one
		@api.depends("slines")
		def _get_total_payment_inaccount(self):
			if self.slines:
				self.total_payment_inaccount=sum(e.amount for e in self.slines if e.payment_type=='inaccount' and  e.transaction_type=='payment')
		

		@api.one
		@api.depends("slines")
		def _get_total_refund_checkout(self):
			if self.slines:
				self.total_refund_checkout=sum(e.amount for e in self.slines if e.payment_type=='checkout' and  e.transaction_type=='refund')
		
		@api.one
		@api.depends("slines")
		def _get_total_refund_inaccount(self):
			if self.slines:
				self.total_refund_inaccount=sum(e.amount for e in self.slines if e.payment_type=='inaccount' and  e.transaction_type=='refund')
		

		@api.one
		@api.depends("slines")
		def _get_total_dept_checkout(self):            
			if self.slines:
				self.total_dept_checkout=sum(e.amount for e in self.slines if e.payment_type=='checkout' and  e.transaction_type=='collection')

		@api.one
		@api.depends("slines")
		def _get_total_debt_bank(self):            
			if self.slines:			    
				self.total_debt_bank=sum(e.amount for e in self.slines if e.payment_type=='bank' and  e.transaction_type=='collection')
		
		@api.one
		@api.depends("total_payment_inaccount","total_payment_bank")
		def _get_total_dept(self):			
				self.total_dept=self.total_dept_checkout+self.total_debt_bank
			
		
		@api.one
		@api.depends("total_payment_checkout","total_payment_bank","total_payment_inaccount")
		def _get_total_payment(self):			
				self.total_payment=self.total_payment_checkout+self.total_payment_bank+self.total_payment_inaccount
		

		@api.one
		@api.depends("total_refund_inaccount","total_refund_checkout")
		def _get_total_refund(self):			
				self.total_refund=self.total_refund_inaccount+self.total_refund_checkout

		@api.one
		@api.depends("total_payment_checkout","total_dept","total_refund_checkout")
		def _get_total_checkout(self):			
				self.total_checkout=self.total_payment_checkout-self.total_refund_checkout
		@api.multi	
		def action_do_open(self):
			self.state='open'
		@api.multi	
		def action_do_close(self):
			for x in self.slines:
				if (x.transaction_type=='payment' and x.amount<x.price) :
					if x.organisation:
						x.organisation.debt+=(x.price-x.amount)
					else:
						x.client.debt+=(x.price-x.amount)
				if (x.transaction_type=='payment' and x.payment_type=='inaccount'):
					if x.organisation:
						x.organisation.debt+=x.amount
					else:
						x.client.debt+=x.amount
				if x.transaction_type=='collection':
					if x.organisation:
						x.organisation.debt-=x.amount
					else:
						x.client.debt-=x.amount
				self.state='close'
		
		@api.multi
		def get_organism_detail(self):
			organisations = []
			detail = []
			
			for line in self.slines:
				organisations.append(line.organisation.name)
			organisations = list(set(organisations))
			for organisation in organisations:
				value_inaccount = 0
				value_collection = 0
				org ={}
				for line in self.slines:
					if line.organisation.name == organisation:
						if line.transaction_type=='collection':
							value_collection += line.amount						
						elif line.payment_type == 'inaccount' and line.transaction_type=='payment':
							value_inaccount += line.amount
						
				org = {'name' : organisation,'Encompte':value_inaccount,'Encaissement':value_collection}
				detail.append(org)
			return detail






