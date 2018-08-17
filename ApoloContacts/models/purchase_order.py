# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp


class ApoloContacts_purchase_order(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    
    company_selection = fields.Selection(string='Selection', default="fournisseur",
        selection=[('fournisseur', 'Fournisseur'), ('distributeur', 'Distributeur')],
        compute='_compute_company_selection', readonly=False)
    
    company_type = fields.Selection(string='Company Type',
        selection=[('person', 'Individu'), ('company', 'Company')],
        compute='_compute_company_type', readonly=False)
    
    
    
    @api.one
    def _compute_company_type(self):
        for record in self:
            if self._context.get('select1') == 'company':
                record.company_type = "company"
#             else:
#                 super(ApoloContacts_purchase_order, self)._compute_company_type()
                
                
    @api.one
    def _compute_company_selection(self):
        for record in self:
            if self._context.get('select1') == 'company':
                record.company_selection = "fournisseur"
#             else:
#                 super(ApoloContacts_purchase_order, self)._compute_company_selection()