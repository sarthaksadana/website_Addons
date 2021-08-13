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
        # logger.info("random string----%s", a)
        # logger.info("random string-b------%s", b)
        headers = request.httprequest.headers
        logger.info("headers-------%s",headers)
        logger.info("request-data-------%s",type(headers))
        logger.info("-headers.__dict__---%s", headers.__dict__)

        response={}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}
        logger.info("request-data-------%s",request_data)
        db_name = tools.config['db_name']
        context  = {}
        registry = registry_get(db_name)
        auth_token = headers.get('auth_token')
        logger.info("auth_token---%s",auth_token)


        issue_name=request_data.get('issue_name')
        comment=request_data.get('comment')
        if auth_token and issue_name:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                        student_obj = env['res.users'].sudo().search([('auth_token', '=', auth_token)])
                        

                        if student_obj:
                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token "
                            })
                            student_objec = env[a].sudo().create({

                                'name' : issue_name,

                                })
                            # logger.info("Objec----%s", student_objec)
                            for i in range (len(comment)):
                                student_objec.sudo().write({
                                    'comment_ids' : [(0,0,{
                                        'issue_id': student_objec.id,
                                        'comment': comment[i]
                                        })]
                                
                                    })
                            logger.info("random string----%s",student_objec.id )
                            # student_objec = env[a].sudo().create({
                            #     'name' : issue_name,
                            #     'comment_ids' : [(0,0,{
                            #         'issue_id':13,
                            #         'comment': "Random comment"
                            #         })]
                            #     })
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

                        if student_obj:
                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token"
                            })
                            student_objec = env['bugfix.menu.report'].sudo().search([('id', '=', issue_id)])
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


    @http.route('/api/v3/model/create', auth='none', csrf=False, type='http',methods=['POST'])
    def static_data(self,**kwargs):
        response={}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}
        headers = request.httprequest.headers

        db_name = tools.config['db_name']
        context  ={}
        registry = registry_get(db_name)
        auth_token = headers.get('auth_token')
        data = request_data.get('data')
        model=request_data.get("model")
        if auth_token:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                        student_obj = env['res.users'].sudo().search([('auth_token', '=', auth_token)])
                        logger.info("student_obj***%s",student_obj)

                        if student_obj:
                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token"
                            })
                            student_objec = env[model].sudo().create(data)
                            logger.info("student_objec***%s",student_objec)
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

    @http.route('/api/v4/model/create', auth='none', csrf=False, type='http',methods=['POST'])
    def Issue_data(self,**kwargs):
        response={}
        request_data = request.httprequest.data and json.loads(request.httprequest.data.decode('utf-8')) or {}
        headers = request.httprequest.headers
        db_name = tools.config['db_name']
        context  ={}
        registry = registry_get(db_name)
        auth_token = headers.get('auth_token')
        data = request_data.get('data')
        model=request_data.get("model")
        if auth_token:
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                        student_obj = env['res.users'].sudo().search([('auth_token', '=', auth_token)])

                        if student_obj:
                            response.update({
                                "status": 200,
                                "Message" : "Valid auth_token"
                            })

                            data_final={}
                            for key in data:
                                a=data[key]
                                if a["type"] == "Many2many":
                                    temp=a["value"]
                                    data_final[key]=[tuple(temp)]

                                elif a["type"] == "One2many":
                                    temp = a["value"]
                                    data_final[key] = [tuple(temp)]

                                else:
                                    data_final[key]=a["value"]
                            logger.info("Datafinal**%s",data_final)


                                # for k in a:
                                #     if k == "type" and  a[k] == "Many2many":
                                #         data_final["value"]=tuple(a[k])
                                #         logger.info("if****%s",data_final) 
                                #     else:
                                #         data_final[v]=a[v]
                                #         logger.info("data_final*********%s",data_final)


               #1.in the loop we have a dict (data[k])
               #2.Inside thatwe have two key value pairs.
               #3.Check if type is many2many,then convert the list in the value key to tuple
               #4.Set a key k in data final having value equal to this new tuple
               #5 else if type is not many2many simply add key k in data final with corresponding to 

                            student_objec = env[model].sudo().create(data_final)
                            logger.info("student_objec***%s",student_objec)
                        else:
                            response.update({
                                "status": 404,
                                "Message" : "InValid auth_token"
                            })

                except Exception as e :
                    logger.info("e::::::::::::::::%s", e, exc_info=True)
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
        
    














