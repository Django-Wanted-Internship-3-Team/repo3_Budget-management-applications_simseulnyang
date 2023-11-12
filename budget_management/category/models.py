from django.db import models


class Category(models.Model):
    STATUS_TYPE = [
        ("in_use", "Category in use"),
        ("delete", "Category deleted"),
    ]

    category_name = models.CharField(max_length=20)
    is_status = models.CharField(max_length=20, choices=STATUS_TYPE, default="in_use")

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "category"
