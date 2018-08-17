# ApoloContacts application

import time
import datetime
import re
import json
import urllib

from odoo import api, fields, models, exceptions, tools, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.fields import One2many, Many2one
from datetime import datetime, date, time, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import logging



class ApoloContacts_kanban_res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    prenom = fields.Char('Prenom')
