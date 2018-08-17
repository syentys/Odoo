from odoo import api, fields, models, exceptions, tools, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.fields import One2many, Many2one
from datetime import datetime, date, time, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP

from calendar import isleap
import logging

#le loggeur
_logger = logging.getLogger('loggeur >>>>>>')
_logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(value)s')
ch.setFormatter(formatter)
# add the handlers to the logger
_logger.addHandler(ch)    

class ApoloContacts_sale_order(models.Model):
    """
    Name of the Class\\: res.partner.category\n
    Inherited class from odoo source code res.partner.category      
    """
    
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    @api.multi
    def action_confirm(self):
        if self.partner_id.prospect == True:
            self.partner_id.prospect = False
        return super(ApoloContacts_sale_order, self).action_confirm()
    
    
    
    
    
    