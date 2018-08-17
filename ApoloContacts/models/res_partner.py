# -*- coding: utf-8 -*-

"""
ApoloContacts -- GoogleMap Location
===================================

.. note:: 
   Module for ODOO. Customization of the module contact according to the specifications \ **APOLO Project** \ . 
 
    **platform** \\: Windows, Linux\n
    **Author** \\: SYENTYS
    info@syentys.com\n
    http://www.syentys.com
"""


import json
import urllib
from datetime import datetime

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


def geo_find(addr):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += urllib.quote(addr.encode('utf8'))

    try:
        result = json.load(urllib.urlopen(url))
    except Exception as e:
        raise UserError(_('Impossible de contacter le serveur. Merci de bien vouloir vérifier vos accés à internet afin de pouvoir effectuer un nouvel essai (%s).') % e)
    if result['status'] != 'OK':
        return None

    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(filter(None, [street,
                                              ("%s %s" % (zip or '', city or '')).strip(),
                                              state,
                                              country])))


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    date_localization = fields.Date(string='Geolocation Date')
    google = fields.Html(compute='generate_google_tag', sanitize=False, sanitize_style=False)

    @api.multi
    def generate_google_tag(self):
        for record in self:
            record.google = '<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d10736.747299414435!2d'+str(record.partner_longitude)+"!3d"+str(record.partner_latitude)+'!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2sus!4v1480002907555" class="div_google_map" width="70%" ></iframe>'

    @api.multi
    def geo_localize(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = geo_find(geo_query_address(street=partner.street,
                                                zip=partner.zip,
                                                city=partner.city,
                                                state=partner.state_id.name,
                                                country=partner.country_id.name))
            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner),
                })
        return True
    
    property_product_pricelist_id = fields.Integer('ID de la pricelist', readonly=True, default=1)
    
    @api.model
    def create(self, vals):
        if vals.get('property_product_pricelist'):
            vals['property_product_pricelist_id'] = vals['property_product_pricelist']
        return super(ResPartner, self).create(vals)
 
    @api.multi
    def write(self, vals):
        if vals.get('property_product_pricelist'):
            vals['property_product_pricelist_id'] = vals['property_product_pricelist']
        return super(ResPartner, self).write(vals)