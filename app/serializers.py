from rest_framework import serializers
from .models import Flow


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        # fields = "__all__"
        fields = ['organization_id','flow_type','purchase_content','operator','init_amount','price','now_amount','create_time']