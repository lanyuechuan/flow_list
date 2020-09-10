import rest_framework_filters as filters
from .models import Flow


class FlowFilter(filters.FilterSet):
    class Meta:
        model = Flow
        fields = {
            'id': ['exact', 'in'],
            'organization_id': ['exact'],
            'flow_type': ['exact'],
            'purchase_content': ['exact'],
            'operator': ['exact'],
            'init_amount': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'price': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'now_amount': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'create_time': ['exact', 'lt', 'gt', 'lte', 'gte']
        }
