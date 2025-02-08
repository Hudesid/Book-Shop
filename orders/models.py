from django.db import models
from django.db.models import TextChoices


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(BaseModel):

    class StatusChoice(TextChoices):
        Success = 'success', 'Success'
        Pending = 'pending', 'Pending'
        Failed = 'failed', 'Failed'

    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='orders')
    book = models.ForeignKey('books.Book', on_delete=models.PROTECT, related_name='orders')
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, default=StatusChoice.Pending, choices=StatusChoice.choices)

    def __str__(self):
        return self.status

#
# class OrderItem(BaseModel):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     book = models.ForeignKey('books.Book', on_delete=models.PROTECT, related_name='orders')
#     quantity = models.IntegerField()
