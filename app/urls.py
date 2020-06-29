from django.urls import path,re_path, include
from rest_framework import routers
from .views import FlowView

from rest_framework.documentation import include_docs_urls # api文档

# 声明一个默认的路由注册器
router = routers.DefaultRouter()
# 注册定义好的接口视图
router.register('flow', FlowView)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs', include_docs_urls(title='账单流水接口文档'))
]
