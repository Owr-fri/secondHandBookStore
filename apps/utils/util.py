import json
from rest_framework import status
from json.encoder import JSONEncoder
from django.http.response import HttpResponse
from rest_framework.response import Response


# 查询成功
def response_success(code=None, message=None, data=None):
    return HttpResponse(json.dumps({
        'code': code,  # code由前后端配合指定
        'msg': message,  # 提示信息
        'data': data,  # 返回数据
        # 'count': len(data )# 总条数
    }, cls=JSONEncoder), 'application/json')


# 查询失败
def response_failure(code=None, message=None, data=None):
    return HttpResponse(json.dumps({
        'code': code,
        'msg': message,
    }), 'application/json')


# 检测用户是否登录
def checkLogin(func):
    """
    查看session值用来判断用户是否已经登录
    :param func:
    :return:
    """

    def warpper(self, request, *args, **kwargs):
        if request.session.get('_auth_user_id', None):
            return func(self, request, *args, **kwargs)
        else:
            return Response({'error': '用户未登录', 'code': 401}, status=status.HTTP_401_UNAUTHORIZED)

    return warpper


def reformUserInfo(user):
    return dict(id=user['id'], user_name=user['first_name'], avatar=user['avatar'],
                chenghu=user['nickname'][0] + '先生' if user['gender'] else user['nickname'][0] + '女士' if user[
                    'nickname'] else '暂无', phone=user['phone'][:7] + r'****' if user['phone'] else '暂无',
                sendAddress=user['sendaddress'], email=user['email'])
