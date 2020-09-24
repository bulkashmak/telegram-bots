from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='user ID in social media',
        unique=True)
    name = models.CharField(verbose_name='Username',
                            max_length=50,
                            null=True,
                            blank=True)

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Profile'


class Message(models.Model):
    profile = models.ForeignKey(Profile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    text = models.TextField(verbose_name='text')
    created_at = models.DateTimeField(verbose_name="receive time",
                                      auto_now_add=True)

    def __str__(self):
        return f'Message {self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Message'
