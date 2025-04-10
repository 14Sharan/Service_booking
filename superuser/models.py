from django.db import models
from accounts.models import User

class ServiceCategory(models.Model):
    category_title = models.CharField(max_length=255,blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_by",null=True,blank=True)

    class Meta:
        managed = True
        db_table = "tb_service_category"

