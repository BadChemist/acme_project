from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from birthday.validators import real_age

MODEL_REPR_LENGTH = 21

User = get_user_model()


class Tag(models.Model):
    tag = models.CharField('Метка', max_length=20)

    def __str__(self):
        return self.tag[:MODEL_REPR_LENGTH]


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField(
        'Фото', upload_to='birthdays_images', blank=True
    )
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
        )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint'
                ),
            )

    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    created_at = models.DateTimeField(
        'Время и дата публикации', auto_now_add=True
        )
    birthday = models.ForeignKey(
        Birthday,
        verbose_name='День рождения',
        on_delete=models.CASCADE,
        related_name='congratulations',
        )
    author = models.ForeignKey(
        User,
        verbose_name='Автор поздравления',
        on_delete=models.CASCADE,
        )

    class Meta:
        ordering = ('created_at',)
