from django.db import models
from django.contrib.auth.models import User
from django import utils

def image_upload_handler(instance, filename):
    return 'profileimg/%s/%s' % (instance.user.id, filename)


class MakeUser(models.Model):
    user = models.OneToOneField(User)   #create one to one field for user
    job_title = models.CharField(max_length=30, null=False, blank=False)    #create field for for job title
    accept_term_condition = models.BooleanField(default=False)  #confirms whether or not user has made the choice to accepted
    photo = models.ImageField(upload_to=image_upload_handler, null=True, blank=True)

    def __unicode__(self):
        return '{}, the {}'.format(self.user, self.job_title)


class RecordTime(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, default='0')
    TIMESTAMP_TYPE_CHOICES = (
        ('I', 'IN'),
        ('O', 'OUT'),
    )
    tstamp = models.DateTimeField(default=utils.timezone.now,
                                  blank=True
                                  )
    type = models.CharField(
        max_length=1,
        choices=TIMESTAMP_TYPE_CHOICES,
        default='O')
