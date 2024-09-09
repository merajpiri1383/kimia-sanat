from django.db import models
from uuid import uuid4

class Item(models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    key = models.CharField(max_length=256,verbose_name="کلید")

    value = models.TextField(verbose_name="مقدار")

    class Meta : 
        abstract = True

    def __str__(self) : 
        return str(self.key)