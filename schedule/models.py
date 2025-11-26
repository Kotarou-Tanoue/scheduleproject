from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    title = models.CharField(
        verbose_name = 'カテゴリー',
        max_length = 20
    )

    def __str__(self):
        return self.title

class SchedulePost(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name = 'ユーザー',
        on_delete = models.CASCADE
    )

    title = models.CharField(
        verbose_name = 'タイトル',
        max_length = 50
    )

    start_date = models.DateField(
        verbose_name = '開始日'
    )

    end_date = models.DateField(
        verbose_name = '終了日'
    )

    category = models.ManyToManyField(
        Category,
        verbose_name = 'カテゴリー',
        blank = True
    )

    location_at = models.CharField(
        verbose_name = '場所',
        max_length = 200,
        blank = True
    )

    comment = models.TextField(
        verbose_name = 'コメント',
        blank = True
    )

    posted_at = models.DateTimeField(
        verbose_name = '追加日時',
        auto_now_add = True
    )


    def __str__(self):
        return self.title