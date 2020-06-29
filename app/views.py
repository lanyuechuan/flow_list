from rest_framework import mixins
from rest_framework import viewsets
from .models import Flow
from .serializers import FlowSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

class FlowView(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """流水get和post接口"""
    queryset = Flow.objects.all()  # 具体返回的数据
    serializer_class = FlowSerializer  # 指定过滤的类
    filter_backends = [DjangoFilterBackend]  # 采用哪个过滤器
    filterset_fields = ['organization_id','flow_type','purchase_content','operator','init_amount','price','now_amount','create_time']  # 进行查询的字段

    def create(self,request):
        data = request.data.copy()
        organization_id = data.get('organization_id')
        flow_type = data.get("flow_type")  # 流水类型
        # init_amount = data.get("init_amount") # 初始金额
        price = int(data.get("price"))  # 变动金额
        obj = Flow.objects.filter(organization_id=organization_id).first()
        # 如果是第一次创建流水，需要设置初始余额
        if not obj:
            init_amount = 0
            if flow_type:
                now_amount = init_amount + price
            else:
                now_amount = init_amount - price
            data['now_amount'] = now_amount
            data['init_amount'] = init_amount
            print(data)
            serializer = FlowSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 如果不是第一次创建
        data['init_amount'] = obj.now_amount
        if flow_type:
            now_amount = obj.now_amount + price
        else:
            now_amount = obj.now_amount - price
        data['now_amount'] = now_amount
        serializer = FlowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)