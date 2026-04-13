from django.db import models
from django.conf import settings

# Create your models here.
class FavsJobs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fav_jobs')
    job_id  = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'job_id')