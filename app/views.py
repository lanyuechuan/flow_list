from rest_framework import mixins
from rest_framework import viewsets
from .models import Flow
from .serializers import FlowSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from .filters import FlowFilter
# Create your views here.

class MyPageNumberPagination(PageNumberPagination):
    """普通分页类"""
    # 每页展示多少条数据
    page_size = 4
    # 前端可以自己通过修改page=10，取哪一页的数据。
    page_query_param = 'page'
    # 前端可以?size=10000自己配置，每页想取多少条自己设置
    page_size_query_param = 'size'
    # 最大页码的查询参数名
    max_page_size = 1000


class FlowView(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """流水get和post接口"""
    queryset = Flow.objects.all()  # 具体返回的数据
    serializer_class = FlowSerializer  # 指定过滤的类
    # filter_backends = [DjangoFilterBackend]  # 采用哪个过滤器
    # filterset_fields = ['organization_id','flow_type','purchase_content','operator','init_amount','price','now_amount','create_time']  # 进行查询的字段
    filter_class = FlowFilter
    search_fields = ('=id',)
    ordering_fields = ('now_amount','create_time')
    pagination_class = MyPageNumberPagination


    def perform_create(self, serializer):
        serializer.save(init_amount=self.request.data.get('init_amount'))

    def create(self,request):
        data = request.data.copy()
        organization_id = data.get('organization_id')
        flow_type = data.get("flow_type")  # 流水类型
        # init_amount = data.get("init_amount") # 初始金额
        price = float(data.get("price"))
        obj = Flow.objects.filter(organization_id=organization_id).order_by('-create_time').first()
        # 如果是第一次创建流水，需要设置初始余额
        if not obj:
            init_amount = 0
            if flow_type == "1":
                now_amount = init_amount + price
            else:
                now_amount = init_amount - price
            data['now_amount'] = now_amount
            data['init_amount'] = init_amount
            serializer = FlowSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 如果不是第一次创建，说明流水中已经存在该组织id
        data['init_amount'] = obj.now_amount
        if flow_type == "1":
            now_amount = data['init_amount'] + price
        else:
            now_amount = data['init_amount'] - price
        data['now_amount'] = now_amount
        serializer = FlowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)