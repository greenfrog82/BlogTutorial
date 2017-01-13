from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # 이게 html 템플릿에서 {{ }}에 Post객체를 감싸서 전달하면 호출되는 부분
    def __str__(self):
        # return self.title
        return 'title : %s\ncreated_date : %s\npublished_date : %s\n' % (self.title, self.created_date, self.published_date)