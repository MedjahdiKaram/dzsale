from openerp import api, models

def get_organism_details():
        return "hello world"


class DzsaleSaleReport(models.AbstractModel):
    _name = 'report.dzsale.dzsale.dailysale_report'


    @api.multi
    def render_html(self, data=None):
        report = self.env['report']._get_report_from_name('dzsale.dailysale_report')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env['dzsale.sale'].search(self._ids),
            'get_organism_details': get_organism_details
            }

        return self.env['report'].render('dzsale.dailysale_report', docargs)

    
DzsaleSaleReport()