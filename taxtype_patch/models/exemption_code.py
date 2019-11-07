# -*- coding: utf-8 -*-
from odoo import models, fields,api
import odoo.addons.decimal_precision as dp


class ExemptionCode(models.Model):

    _name = "exemption.reason.code"

    x_name = fields.Char(string="Name")
    x_code = fields.Char(string="Code")
