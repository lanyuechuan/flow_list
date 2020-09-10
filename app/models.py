from django.db import models
from lib import create_objectid

# Create your models here.

"""
流水类型：
0代表支出
1代表充值
2代表赠送
"""


class Flow(models.Model):
    """账单流水"""
    id = models.CharField(verbose_name="id",primary_key=True,max_length=24,default=create_objectid())
    organization_id = models.CharField(verbose_name="组织机构id", max_length=64)
    flow_type = models.CharField(verbose_name="流水类型", max_length=1,blank=True)
    purchase_content = models.CharField(verbose_name="变动原因", max_length=32, blank=True, null=True)
    operator = models.CharField(verbose_name="操作人员", max_length=64)
    init_amount = models.FloatField(verbose_name="起始金额")
    price = models.FloatField(verbose_name="变动金额")
    now_amount = models.FloatField(verbose_name="最后金额")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


    def __str__(self):
        return self.organization_id

    # class Meta:
    #     # db_table = "db_flow"
    #     # verbose_name = "账单流水"
    #     verbose_name_plural = verbose_name
