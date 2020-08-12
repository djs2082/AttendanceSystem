
from Attendance import settings
from rest_framework.views import APIView
import jwt
from requirements import error
from rest_framework.response import Response
from requirements import success,error
class Authentication(APIView):
    def __init__(self):
        self.key=settings.SECRET_KEY
        self.algorithm='HS256'
    def create_token(self,user,id,email):
        try:
            token=jwt.encode({'user':user,'user_id':id,'email':email},self.key,self.algorithm)
            return({'Status':200,'Token':token.decode('utf-8')})
        except Exception as unknown_exception:
            return({'Status':502,'Error':str(unknown_exception),'message':'error occoured in processing at server'})


    def get(self,request,token):
        try:
            data=jwt.decode(token,self.key,'utf-8',self.algorithm)
            success_message=data
            response=success.APIResponse(202,success_message).respond()
            return Response(response)
        except jwt.InvalidTokenError as err:
            return Response(error.APIErrorResponse(400,str(err)).respond())
        except Exception as err:
            return Response(error.APIErrorResponse(400,str(err)).respond())
