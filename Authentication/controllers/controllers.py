from odoo import api, fields, models, tools,SUPERUSER_ID, _
from odoo import http
from odoo.http import request
import json
import xml.etree.ElementTree as ET
from ast import literal_eval
from odoo import registry as registry_get
import logging
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.portal.controllers.portal import CustomerPortal
logger = logging.getLogger(__name__)
import werkzeug
import string
import random
from odoo.osv import expression
import hashlib
from datetime import datetime



class Authentication(http.Controller):
    @http.route('/api/authentication/', auth='none', csrf=False, type='http',methods=['POST'])
    def cert_auth(self,**kwargs):
        response =  {}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}

        db_name = tools.config['db_name']
        context  ={}
        registry = registry_get(db_name)
        issuer_id = request_data.get('issuer_id')
        password = request_data.get('password')
        if issuer_id and password:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                    t = env['res.users'].sudo()._login(db_name, issuer_id, password,{})
                    if t:
                        student_obj = env['res.users'].sudo().search([('id', '=', t)])
                        # if student_obj.auth_token:
                        #     auth = student_obj.auth_token
                        # else:
                        #     # get current datetime  + email
                        now = datetime.now()
                        str2hash = now.strftime("%Y%m%d %H:%M:%S.%f")
                        str2hash+=student_obj.login

                        result = hashlib.md5(str2hash.encode())
                        auth = result.hexdigest()

                        student_obj.write({
                            'auth_token': auth
                        })

                        response.update({
                            "status": 200,
                            "auth": auth,
                            "error_msg": False
                        })
                except Exception as e :
                    # _logger.info("e::::::::::::::::%s", e, exc_info=True)
                    response.update({
                        "status" :404,
                        "auth": False,
                        "error_msg": str(e),
                    })
        else:
            response.update({
                "status":404,
                "auth": False,
                "error_msg":"Invalid request",
            })

        # return self._response("dynamic_route", response)
        return json.dumps(response)

    @http.route('/api/get_data/', auth='none', csrf=False, type='http',methods=['GET'])
    def get_data(self,**kwargs):
        response =  {}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}

        db_name = tools.config['db_name']
        context  ={}
        registry = registry_get(db_name)
        auth_token = request_data.get('auth_token')
        if auth_token:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                        student_obj = env['res.users'].sudo().search([('auth_token', '=', auth_token)])
                        if student_obj:
                            # auth = student_obj.auth_token
                        # else:
                            # get current datetime  + email
                            # now = datetime.now()
                            # str2hash = now.strftime("%Y%m%d %H:%M:%S.%f")
                            # str2hash+=student_obj.login

                            # result = hashlib.md5(str2hash.encode())
                            # auth = result.hexdigest()

                            # student_obj.write({
                            #     'auth_token': auth
                            # })

                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token"
                            })
                        else:
                            response.update({
                                "status": 404,
                                "Message" : "InValid auth_token"
                            })

                except Exception as e :
                    # _logger.info("e::::::::::::::::%s", e, exc_info=True)
                    response.update({
                        "status" :402,
                        "auth": False,
                        "error_msg": str(e),
                    })
        else:
            response.update({
                "status":404,
                "auth": False,
                "error_msg":"Invalid request",
            })

        # return self._response("dynamic_route", response)
        return json.dumps(response)
    

    @http.route('/api/v1/<a>/<b>', auth='none', csrf=False, type='http',methods=['POST'])
    def data_auth(self,a,b,**kwargs):
        logger.info("random string----%s", a)
        logger.info("random string-b------%s", b)
        response={}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}

        db_name = tools.config['db_name']
        context  ={}
        registry = registry_get(db_name)
        auth_token = request_data.get('auth_token')
        issue_name=request_data.get('issue_name')
        if auth_token and issue_name:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                        student_obj = env['res.users'].sudo().search([('auth_token', '=', auth_token)])
                        

                        if student_obj:
                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token and issue name updated"
                            })
                            student_objec = env[a].sudo().create({'name' : issue_name})
                        else:
                            response.update({
                                "status": 404,
                                "Message" : "InValid auth_token"
                            })

                except Exception as e :
                    # _logger.info("e::::::::::::::::%s", e, exc_info=True)
                    response.update({
                        "status" :402,
                        "auth": False,
                        "error_msg": str(e),
                    })
        else:
            response.update({
                "status":404,
                "auth": False,
                "error_msg":"Invalid request",
            })
    
        return json.dumps(response)
        # request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}
    
    @http.route('/api/v2/<a>/<b>', auth='none', csrf=False, type='http',methods=['POST'])
    def auth_data(self,a,b,**kwargs):
        logger.info("random string----%s", a)
        logger.info("random string-b------%s", b)
        response={}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}

        db_name = tools.config['db_name']
        context  ={}
        registry = registry_get(db_name)
        auth_token = request_data.get('auth_token')
        issue_id=request_data.get('issue_id')
        comment=request_data.get('comment')
        if auth_token:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                        student_obj = env['res.users'].sudo().search([('auth_token', '=', auth_token)])
                        student_objec = env['bugfix.menu.report'].sudo().search([('id', '=', issue_id)])

                        if student_obj :
                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token"
                            })
                            if student_objec:
                                student_object = env[a].sudo().create({'comment': comment ,"issue_id" : issue_id })
                                response.update({
                                    "status" : 200,
                                    "Message" : "comment updated"
                                    })
                            
                        else:
                            response.update({
                                "status": 404,
                                "Message" : "InValid auth_token"
                            })

                except Exception as e :
                    # _logger.info("e::::::::::::::::%s", e, exc_info=True)
                    response.update({
                        "status" :402,
                        "auth": False,
                        "error_msg": str(e),
                    })
        else:
            response.update({
                "status":404,
                "auth": False,
                "error_msg":"Invalid request",
            })
    
        return json.dumps(response)

        
    

