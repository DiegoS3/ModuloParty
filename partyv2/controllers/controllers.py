# -*- coding: utf-8 -*-
# from odoo import http


# class Partyv2(http.Controller):
#     @http.route('/partyv2/partyv2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partyv2/partyv2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partyv2.listing', {
#             'root': '/partyv2/partyv2',
#             'objects': http.request.env['partyv2.partyv2'].search([]),
#         })

#     @http.route('/partyv2/partyv2/objects/<model("partyv2.partyv2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partyv2.object', {
#             'object': obj
#         })
