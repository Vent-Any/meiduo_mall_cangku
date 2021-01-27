from rest_framework.response import Response


def jwt_response_payload_handler(token, user=None, request=None):
    # 控制数据返回的方法
    return {
        'token': token,  # 系统生成
        'username': user.username,
        'user_id': user.id
    }


from rest_framework.pagination import PageNumberPagination

# 分页
class PageNumber(PageNumberPagination):
    page_size = 2  # 设置一页多少数据  必须设置,设置它就相当于开启了分页
    page_size_query_param = 'pagesize'  # 设置前段的请求参数

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'lists': data,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'pagesize': self.page_size,
        })
