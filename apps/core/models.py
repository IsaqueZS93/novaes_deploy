from django.db import models

class TimeStampedModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

class ActiveModel(models.Model):
    is_active=models.BooleanField(default=True)
    class Meta:
        abstract=True

class CenterCost(TimeStampedModel,ActiveModel):
    name=models.CharField(max_length=150,unique=True)
    description=models.TextField(blank=True)
    def __str__(self):
        return self.name

class Attachment(TimeStampedModel):
    module_reference=models.CharField(max_length=50)
    record_id=models.PositiveIntegerField()
    file=models.FileField(upload_to='attachments/%Y/%m/')
    uploaded_by=models.ForeignKey('accounts.User',on_delete=models.SET_NULL,null=True)

class MovementHistory(TimeStampedModel):
    module=models.CharField(max_length=60)
    record_id=models.PositiveIntegerField()
    action=models.CharField(max_length=30)
    description=models.TextField()
    user=models.ForeignKey('accounts.User',on_delete=models.SET_NULL,null=True)
    occurred_at=models.DateTimeField(auto_now_add=True)
