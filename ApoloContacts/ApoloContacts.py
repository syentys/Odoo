# -*- coding: utf-8 -*-
# ApoloContacts application

"""
ApoloContacts -- Contacts Apolo Project
=======================================

.. note:: 
   Module for ODOO. Customization of the module contact according to the specifications \ **APOLO Project** \ . 
 
    **platform** \\: Windows, Linux\n
    **Author** \\: SYENTYS
    info@syentys.com\n
    http://www.syentys.com
    
.. list-table:: **Maintenance History**
   :widths: 10 10 10 20 40
   :header-rows: 1
   :stub-columns: 0

   * - Date
     - Version
     - Commit
     - Author
     - Comment
   * - 01/10/2016
     - 1.0
     - N/C
     - GBAUER
     - Some Function must be improved
   * - 16/01/2017
     - 1.0
     - N/C
     - GBAUER
     - Add Sphinx autodoc
     
"""

import time
import datetime
import re
import json
import urllib
import dateutil.parser

from odoo import api, fields, models, exceptions, tools, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.fields import One2many, Many2one
from datetime import datetime, date, time, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP

from calendar import isleap
import logging
_logger = logging.getLogger(__name__)


class ApoloContacts_res_partner_category(models.Model):
    """
    Name of the Class\\: res.partner.category\n
    Inherited class from odoo source code res.partner.category      
    """
    
    _name = 'res.partner.category'
    _inherit = 'res.partner.category'
    
    ref_cat_contact = fields.Char(u'Référence catégorie')
    

class ApoloContacts_res_partner(models.Model):
    """
    Name of the Class\\: res.partner\n
    Inherited class from odoo source code res.partner      
    """
    
    
    _name = 'res.partner'
    _inherit = 'res.partner'

    praticien = fields.Boolean('Praticien')
    """
    This field indicate if the customer is a praticien
    
        :type boolean: *True* or *False*
    """
    prospect = fields.Boolean('Prospect')
    """
    This field indicate if the customer is a prospect
    
        :type boolean: *True* or *False*
    """
    fournisseur = fields.Boolean('Fournisseur', related='supplier', store=True)
    """
    This field indicate if the contact is a supplier
    
        :type boolean: *True* or *False*
        
        :param related: field related to supplier (odoo code)
        
        :param store: True
    """
    distributeur = fields.Boolean('Distributeur')
    """
    This field indicate if the customer is a distributor
    
        :type boolean: *True* or *False*
    """
    codeINSEE = fields.Char('Code INSEE', default='00000')
    """
    This field indicate if the customer is a praticien
    
        :type Char: User enter the INSEE code for the customer's town. The function length_codeINSEE control the length (max 5 characters) and the type (only integer)
    """
    diplome = fields.Char('Diplome')
    """
    This field indicate if the customer is a praticien
    
        :type char: Fill the field with the dentist's degree
    """
    annee_diplome = fields.Datetime()
    """
    choose the graduation date
    
        :type datetime: Date of graduation, use in couple with diploma
    """
    prenom = fields.Char('Prenom')
    """
    Additional field for customer information
    
        :type char: Dedicate to the customer's firstname
    """
    bloque = fields.Boolean('bloque')
    """
    This field indicate if the contact have some financial difficulties
    
        :type boolean: *True* or *False*
    """
    fclient = fields.Boolean('Client', related='customer', store=True)
    """
    This field replaces the client field with original client settings
    
        :type boolean: *True* or *False*
        :param related: field related to customer (odoo code)
        :param store: True
    """
    duplicate_name = fields.Char('Nom', related='name', store=True)
    """
    This field replaces the name field with original name settings
    
        :type char: Not display but use with the compute function use to test the duplicate entries
        :param related: field related to name (odoo code)
        :param store: True
    """
    duplicate_phone = fields.Char('Telephone', related='phone', store=True, required=True)
    """
    This field replaces the phone field with original phone settings
    
        :type char: Not display but use with the compute function use to test the duplicate entries
        :param related: field related to phone (odoo code)
        :param store: True
    """
    duplicate_category_id = fields.Many2many(related='category_id')
    """
    This field replaces the category_id field with original category_id settings
    
        :type Many2many: use for test, not display
        :param related: field related to category_id (odoo code)
    """
    
   
    individu_selection = fields.Selection(string='Selection', default='praticien',
        selection=[('praticien', 'Praticien'), ('prospect', 'Prospect')],
        required=True)
    """
    This field let the user to indicate if the contact is a customer Praticien or Prospect (no sale at this moment).\n
    Choose one hide some field not required for the selected item.
    
        :type selection: praticien is set by default
        :param required: True 
    """

    company_selection = fields.Selection(string='Selection',
        selection=[('fournisseur', 'Fournisseur'), ('distributeur', 'Distributeur')],
        readonly=False)
    """
    This field let the user to indicate if the contact is a supplier or a distributor.\n
    Choose one hide some field not required for the selected item.
    
        :type selection: supplier or distributor
        :param compute: the compute function *compute_company_selection* set by default to supplier
        :param readonly: False
        
    .. warning:: This compute function is not working. Solution to be find but just for improving the module.
    """

    favorite_ids = fields.Many2many('product.template', string='Favorite Products')

    #**********************************
    #Declaration des jours d'ouverture*
    #**********************************
    
    lundi_am = fields.Float()
    mardi_am = fields.Float()
    mercredi_am = fields.Float()
    jeudi_am = fields.Float()
    vendredi_am = fields.Float()
    samedi_am = fields.Float()
    lundi_pm = fields.Float()
    mardi_pm = fields.Float()
    mercredi_pm = fields.Float()
    jeudi_pm = fields.Float()
    vendredi_pm = fields.Float()
    samedi_pm = fields.Float()
    a_lundi_am = fields.Float()
    a_mardi_am = fields.Float()
    a_mercredi_am = fields.Float()
    a_jeudi_am = fields.Float()
    a_vendredi_am = fields.Float()
    a_samedi_am = fields.Float()
    a_lundi_pm = fields.Float()
    a_mardi_pm = fields.Float()
    a_mercredi_pm = fields.Float()
    a_jeudi_pm = fields.Float()
    a_vendredi_pm = fields.Float()
    a_samedi_pm = fields.Float()
    jours_ouverture = fields.Float()
    """
    The field jours_ouverture is not used but entered for code documentation on 6 business days in a week (except sunday).\n
    +----------------------+---------------------+---------------------+--------------------+       
    |Morning               |Type                 |Evening              |Type                |
    +======================+=====================+=====================+====================+
    |lundi_am              |Float                |a_lundi_pm           |Float               |
    +----------------------+---------------------+---------------------+--------------------+
    |mardi_am              |Float                |a_mardi_pm           |Float               |
    +----------------------+---------------------+---------------------+--------------------+
    |mercredidi_am         |Float                |a_mercredi_pm        |Float               |
    +----------------------+---------------------+---------------------+--------------------+
    |jeudi_am              |Float                |a_jeudi_pm           |Float               |
    +----------------------+---------------------+---------------------+--------------------+
    |vendredi_am           |Float                |a_vendredi_pm        |Float               |
    +----------------------+---------------------+---------------------+--------------------+
    |samedi_am             |Float                |a_samedi_pm          |Float               |
    +----------------------+---------------------+---------------------+--------------------+
    """

    #**************************
    # Declaration des statuts *
    #**************************
    statut = fields.Selection([
                               ('association', 'Association'),
                               ('E.I.','E.I.'),
                               ('E.I.R.L.','E.I.R.L.'),
                               ('E.U.R.L.','E.U.R.L.'),
                               ('S.N.C.','S.N.C.'),
                               ('S.A.','S.A.'),
                               ('S.A.R.L.','S.A.R.L.'),
                               ('S.E.L.A.R.L.','S.E.L.A.R.L.'),
                               ('S.C.P.','S.C.P.'),
                               ('S.A.S.','S.A.S.'),
                               ('S.A.S.U.','S.A.S.U.')
                               ])
    """
    +---------------+---------------+--------------------------------------------------+
    |Selection      |Champ          |Description                                       |
    +===============+===============+==================================================+
    |Association    |Association    |Association                                       |
    +---------------+---------------+--------------------------------------------------+
    |E.I.           |E.I.           |Entreprise Individuelle                           |
    +---------------+---------------+--------------------------------------------------+
    |E.I.R.L.       |E.I.R.L.       |Entreprise Individuelle Responsabilite limitee    |
    +---------------+---------------+--------------------------------------------------+
    |E.U.R.L.       |E.U.R.L.       |Entreprise Unipersonnelle Responsabilite limitee  |
    +---------------+---------------+--------------------------------------------------+
    |S.N.C.         |S.N.C.         |Societe en nom collectif                          |
    +---------------+---------------+--------------------------------------------------+
    |S.A.           |S.A.           |Societe Anonyme                                   |
    +---------------+---------------+--------------------------------------------------+
    |S.A.R.L.       |S.A.R.L.       |Societe A Responsabilite Limitee                  |
    +---------------+---------------+--------------------------------------------------+
    |S.E.L.A.R.L.   |S.E.L.A.R.L.   |Societe Exercice Liberal A Responsabilite Limitee |
    +---------------+---------------+--------------------------------------------------+
    |S.C.P.         |S.C.P.         |Societe Civile Professionnelle                    |
    +---------------+---------------+--------------------------------------------------+
    |S.A.S.         |S.A.S.         |Societe par Action Simplifiee                     |
    +---------------+---------------+--------------------------------------------------+
    |S.A.S.U.       |S.A.S.U.       |Societe par Action Simplifiee unipersonnelle      |
    +---------------+---------------+--------------------------------------------------+
    """


    #******************************
    # Declaration des specialites *   
    #******************************

    specialite_ids = fields.Selection([
                               ('orthodontie', 'Orthodontie'),
                               ('omnipraticien','Omnipraticien'),
                               ('pedodontie','Pedodontie'),
                               ('parodontie','Parodontie'),
                               ('endodontie','Endodontie'),
                               ('implantodontie','Implantodontie'),
                               ('chirurgie Buccale','Chirurgie Buccale'),
                               ('occlusodontie','Occlusodontie'),
                               ('gerontodontie','Gerontodontie'),
                               ('autre','Autre'),
                               ])
    """
    +----------------------+--------------------------------------+
    |Selection             |Description                           |
    +======================+======================================+
    |orthodontie           |Orthodontie                           |
    +----------------------+--------------------------------------+
    |omnipraticien         |Omnipraticien                         |
    +----------------------+--------------------------------------+
    |pedodontie            |Pedodontie                            |
    +----------------------+--------------------------------------+
    |parodontie            |Parodontie                            |
    +----------------------+--------------------------------------+
    |endodontie            |Endodontie                            |
    +----------------------+--------------------------------------+
    |implantodontie        |Implantodontie                        |
    +----------------------+--------------------------------------+
    |chirurgie Buccale     |Chirurgie Buccale                     |
    +----------------------+--------------------------------------+
    |occlusodontie         |Occlusodontie                         |
    +----------------------+--------------------------------------+
    |gerontodontie         |Gerontodontie                         |
    +----------------------+--------------------------------------+
    |autre                 |Autre                                 |
    +----------------------+--------------------------------------+
    """
    
    #**************************
    #  Declaration de SONCAS  *
    #**************************
    soncas = fields.Selection([
                               ('securite', 'Sécurité'),
                               ('orgueil','Orgueil'),
                               ('nouveaute','Nouveauté'),
                               ('confort','Confort'),
                               ('argent','Argent'),
                               ('sympathie','Sympathie'),
                               ])
    """
    +----------------------+--------------------------------------+
    |Selection             |Description                           |
    +======================+======================================+
    |securite              |Securité                              |
    +----------------------+--------------------------------------+
    |orgueil               |Orgueil                               |
    +----------------------+--------------------------------------+
    |nouveaute             |Nouveauté                             |
    +----------------------+--------------------------------------+
    |confort               |Confort                               |
    +----------------------+--------------------------------------+
    |argent                |Argent                                |
    +----------------------+--------------------------------------+
    |Sympathie             |Sympathie                             |
    +----------------------+--------------------------------------+
    """

    #***************************************************************
    # Ajout du champ Employe et modification de person en individu *
    #***************************************************************

    employee_apol = fields.Boolean(string=u"Employé APOL", default=False)

    individu_type = fields.Selection(string='Individu Type', default='independant',
        selection=[('independant', 'Independant'), ('employe', 'Employe')], required=True)
    """
    This field let the user to indicate the individu type is a independant or a employe.\n
    Choose one hide some field not required for the selected item.
    
        :type selection: independant or employe
        :param required: True
        
        
    """
    
    #************************************************************
    #   Champ permettant l'affichage du detail des commandes    *
    #************************************************************
    
    sale_order_ids = fields.One2many('sale.order', 'partner_id', 'Sales Order', store=True )
    """
    This field is used to display order details e.g. product, quantity, price
        :type One2many: related to sale.order, partner_id informations and display the selected item
        :param store: True
    """
    
    pos_order = fields.One2many('pos.order', 'partner_id', 'POS Order', store=True )
    """
    This field is used to display order details
        :type One2many: related to pos.order, partner_id informations and display the selected item
        :param store: True
    """

    #****************************************************
    # Fonction Test de la longueur du champ code INSEE  *
    #****************************************************

    @api.constrains('codeINSEE')
    def length_codeINSEE(self):
        """
        This function test the field code_insee.
        
           :arg len: if code_INSEE len \\!= 5
           :arg type: if code_INSEE type \\!= Integer
           :returns: boolean. True is successful
           :raises: ValidationError: Erreur le code INSEE se compose de cinq chiffres.
        
        .. warning:: this function is \ **required** \ and at this moment theres no possibility to pass through. A solution to be find.
        """
        for object in self:
            if object.codeINSEE == 00000 or len(object.codeINSEE) == 5:
                if object.codeINSEE == int(object.codeINSEE):
                   return True
            else:
                raise ValidationError("Erreur, le Code INSEE se compose de cinq chiffres")
            



    #***************************************************
    #   Test doublons creation des nouveaux contacts   *
    #***************************************************

#     _sql_constraints = [('duplicate_name_uniq', 'unique (duplicate_name,duplicate_phone)',"Le contact que vous enregistrez, semble deja exister. Utilisez le bouton liste pour comparer et fusionner.")]
    """
    This constraint use sql query to test if the new contact already exist.\n
    Test one or more field to check duplicate entries (name and phone).\n
    """
    
    #***************************************************
    #      Fonction affichage vue avec un bouton       *
    #***************************************************

    show_document_count = fields.Integer(compute='_compute_show_document_count', string="Fichier")
    
    @api.multi
    def _compute_show_document_count(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', self._name), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        mapped_data = dict([(data['res_id'], data['res_id_count']) for data in attachment_data])
        for d in mapped_data:
            _logger.error("ATTENTION-WARNING-ACHTUNG "+str(d))
        for res_partner in self:
            res_partner.show_document_count = mapped_data.get(res_partner.id, 0)

    def show_list_customer_to_merge(self):
       
        return {
        'name': ('tree_merge_view'),
        'view_type': 'form',
        'view_mode': 'tree',
        'res_model': 'res.partner',
        'view_id': False,
        'type': 'ir.actions.act_window',
        }
    
    @api.multi    
    def show_document(self):
        self.ensure_one()
        return {
        'name': ('tree_merge_view'),
        'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
        'view_type': 'form',
        'view_mode': 'kanban,form',
        'res_model': 'ir.attachment',
        'type': 'ir.actions.act_window',
        'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id),
        }        
      
    @api.multi    
    def unblock_client(self):
        """
        Function which put the current date in the unblocking_date and reactivate client
        """
        for record in self:
            record.unblocking_date = datetime.today()
            record.bloque = False
#         return {
#         'name': ('tree_merge_view'),
#         'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
#         'view_type': 'form',
#         'view_mode': 'kanban,form',
#         'res_model': 'ir.attachment',
#         'type': 'ir.actions.act_window',
#         'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id),
#         }     
   
   
    #************************************
    #     Date de derniere commande     *
    #************************************
   
    
    
    @api.one
    def _get_max_sale_order_date(self):
        """
        Function using the sale order date to display the date of the last order.\n
        Using the decorator \\@\\api.one this function use the information in the sale_order_ids 
        
           :arg date_list: append date order
           :returns: the last ordering date
        """
        for record in self:
            date_list = list()
            for order in self.sale_order_ids:
                 date_list.append(order.date_order)
        if date_list:
            self.max_sale_order_date = max(date_list)
            
    max_sale_order_date = fields.Datetime(compute='_get_max_sale_order_date', string='Date de la derniere commande de Vente')
            
    @api.one
    def _get_max_pos_order_date(self):
        """
        Last order in POS
           :arg date_list: append date order
           :returns: the last ordering date in pos
        """
        for record in self:
            date_list = list()
            for order in self.pos_order:
                 date_list.append(order.date_order)
        if date_list:
            self.max_pos_order_date = max(date_list)
            
    max_pos_order_date = fields.Datetime(compute='_get_max_pos_order_date', string='Date de la derniere commande du PdV')
    
    @api.one
    def _get_max_order_date(self):
        """
        Last order in POS and sale
           :arg date_list: append date order
           :returns: the last ordering date
        """
        for record in self:
            date_list = list()
            for order in self.sale_order_ids:
                 date_list.append(order.date_order)
            for order_pos in self.pos_order:
                 date_list.append(order_pos.date_order)
        if date_list:
            self.max_order_date = max(date_list)
    
    max_order_date = fields.Datetime(compute='_get_max_order_date', string='Date de la derniere commande')
            
#     @api.one
#     def _get_max_sale_pos_order_date(self):
#         """
#            :arg date_list: append date order
#            :returns: the last ordering date
#         """
#         for record in self:
#             date_list = list()
#             for order in self.sale_order_ids:
#                  date_list.append(order.date_order)
#         if date_list:
#             self.max_sale_order_date = max(date_list)
#     
#     max_sale_pos_order_date = fields.Datetime(compute='_get_max_sale_pos_order_date', string='Date de la derniere commande (sale+POS)')
    
    """
    This field display the last sale order date (This field must be declare after the function to work).
        :type datetime: last sale order date for the current customer.
        :param compute: _get_max_sale_order_date use in the function _get_max_sale_order_date
    """
   
    #***************************************************************************************************************
    #       Catégorie référence, non utilisée
    #***************************************************************************************************************
    """
    @api.onchange('category_id')
    def change_category(self):
        category_ref = [c.ref_cat_contact or "" for c in self.category_id]
        self.category_reference = ", ".join(category_ref)

    def _compute_category_reference(self):
        for partner in self:
            partner.change_category()
                

    category_reference = fields.Char(string=u'Référence catégorie', compute='_compute_category_reference')
    """

    
    #***************************************************************************************************************
    #!!!!!!! Fonction calcul nombre de mois derniere commande pour indiquer client bloque - NON FONCTIONNEL !!!!!!!*
    #***************************************************************************************************************
    """
    d = datetime.today() - timedelta(6*365/12)
    
    
    
    @api.one
    @api.depends('d','bloque')
    def old_order(self):
        for record in self:
            if record.d  <= 6.0:
                if record.d > 0:
                    record.bloque = False
            else:
                record.bloque = True
                
    @api.one
    @api.depends('max_sale_order_date')
    def _partner_is_disabled(self):
        for record in self:
            d = fields.Datetime(datetime.today) - datetime.timedelta(days=6*365/12)
            if self.max_sale_order_date:
                if self.max_sale_order_date < datetime.today():
                    self.inactif = True
                else:
                    self.inactif = False
            
               
    inactif = fields.Boolean(compute='_partner_is_disabled')  
    """
    @api.multi
    @api.depends('max_order_date','bloque','unblocking_date')
    def _partner_is_disabled(self):
        for record in self:
            if record.time_aft_last_order >= 365 :
                if self.more_one_year(record.unblocking_date) :
                    record.inactif = True
                else:
                    record.inactif = False
            else:
                record.inactif = False
               
    inactif = fields.Boolean(compute='_partner_is_disabled')
    
    def more_one_year(self,ref_date):
        """
        This function return true if the ref_date is at least a year old
        """
        if ref_date:
            max_date = datetime.strptime(ref_date, '%Y-%m-%d %H:%M:%S')
            max_date = max_date.replace(year = max_date.year + 1)
            return max_date < datetime.today()
        else:
            return True
    
    time_aft_last_order = fields.Float(compute='_timedelta_order', string="Nb jours depuis la dernière commande")
    """
    This field give the number of days passed since the last order (POS or Sales)
    """
    
    unblocking_date = fields.Datetime(string="Date de la dernière réactivation", readonly=True)
    blocking_date = fields.Datetime(string="Date du dernier blocage", readonly=True)

    @api.multi
    @api.depends('max_order_date','bloque')
    def _timedelta_order(self):
        for record in self:
            if record.max_order_date:
                begin_date = datetime.strptime(record.max_order_date, '%Y-%m-%d %H:%M:%S')
            else:
                begin_date = datetime.today()
            end_date = datetime.today()
            diffyears = end_date.year - begin_date.year
            difference  = end_date - begin_date.replace(end_date.year)
            # days_in_year = isleap(end_date.year) and 366 or 365
            difference_in_days = diffyears*365.25 + (difference.days + difference.seconds/86400.0)   
            record.time_aft_last_order = difference_in_days
  
#     @api.onchange('bloque')
#     def change_bloque(self):
#         if self.bloque:
#             self.blocking_date = datetime.today()
            
    #the next create and write functions allows to have readonly fields which are linked to onchange
    @api.model
    def create(self, vals):
        # if (vals.get('fournisseur') or vals.get('distributeur')) and not self.env.user.id in self.env.ref('account.group_account_user').users.ids:
        #     raise ValidationError(_('Only %s can create suppliers and distributors.') % self.env.ref('account.group_account_user').name)
        if vals.get('bloque'):
            vals['blocking_date'] = datetime.today()
        return super(ApoloContacts_res_partner, self).create(vals)

    @api.multi
    def write(self, vals):
        # if (vals.get('fournisseur') or vals.get('distributeur') or self.fournisseur or self.distributeur) and not self.env.user.id in self.env.ref('account.group_account_user').users.ids:
        #     raise ValidationError(_('Only %s can edit suppliers and distributors.') % self.env.ref('account.group_account_user').name)
        if vals.get('bloque'):
            vals['blocking_date'] = datetime.today()
        return super(ApoloContacts_res_partner, self).write(vals)
    
    @api.multi
    def unlink(self):
        # for partner in self:
        #     if (partner.fournisseur or partner.distributeur) and not self.env.user.id in self.env.ref('account.group_account_user').users.ids:
        #         raise ValidationError(_('Only %s can delete suppliers and distributors.') % self.env.ref('account.group_account_user').name)
        return super(ApoloContacts_res_partner, self).unlink()