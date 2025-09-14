from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator, ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    first_name = models.CharField(max_length=30, verbose_name='Имя', blank=True)
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', blank=True)
    avatar_url = models.URLField(verbose_name="Аватар (из Telegram)", blank=True, null=True)


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username} ({self.last_name})'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Tour(models.Model):

    tour_name = models.CharField(max_length=50, verbose_name='Название экскурсии')
    tour_description = models.TextField(verbose_name='Описание экскурсии',
                                        validators=[MinLengthValidator(10,
                                        message='Минимальная длина описания - 10 символов')])
    tour_img = models.ImageField(upload_to='tours_media/tours_img', null=True, blank=True)
    tour_content_type = models.CharField(default='Экскурсия', editable=False, max_length=10)
    tour_created_time = models.TimeField(auto_now=True, verbose_name='Время создания')
    tour_created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_tour_active = models.BooleanField(default=False)



    class Meta:
        verbose_name = 'Экскурсия'
        verbose_name_plural = 'Экскурсии'
        ordering = ['-tour_created_date']

    def __str__(self):
        return f'{self.tour_name} : {self.tour_created_date}'

class TourDropDownElements(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='drop_down_elements',
        verbose_name='Элементы экскурсии'
    )
    element_name = models.CharField(max_length=100, verbose_name='Название элемента экскурсии')
    element_description = models.TextField(verbose_name='Описание элемента экскурсии', blank=True)
    element_icon = models.ImageField(upload_to='tour_el_media/icons', blank=True, null=True)
    element_created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания элемента экскурсии')
    element_img = models.ImageField(upload_to='tour_el_media/photo', verbose_name='Фото', blank=True, null=True)
    element_video = models.FileField(
        upload_to='tour_el_media/video',
        validators=[FileExtensionValidator(
            allowed_extensions=['mp4', 'mov', 'avi']
        )],
        verbose_name='Видео',
        blank=True,
        null=True)


    class Meta:
        verbose_name = 'Элемент выпадающего списка'
        verbose_name_plural = 'Элементы выпадающего списка'
        ordering = ['element_created_at', 'element_name']

    def __str__(self):
        return f'{self.tour} : {self.element_name}, {self.element_created_at}'
class Quiz(models.Model):

    QUIZ_TYPES = [
        ('text', 'Текстовый ответ'),
        ('single', 'Один вариант из нескольких'),
        ('multiple', 'Несколько вариантов'),
    ]
    quiz_name = models.CharField(max_length=100, verbose_name='Название квиза')
    quiz_description = models.TextField(verbose_name='Описание квиза', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания квиза')
    quiz_type = models.CharField(
        max_length=10,
        choices=QUIZ_TYPES,
        default='text',
        verbose_name='Тип квиза'
    )

    class Meta:
        verbose_name = 'Квиз'
        verbose_name_plural = 'Квизы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.quiz_name} ({self.get_quiz_type_display()} - {self.created_at})'

class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Квиз'
    )

    question_text = models.TextField(verbose_name='Текст вопроса')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок вопроса')


    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order', 'id']

    def __str__(self):
        return f'Вопрос "{self.quiz.quiz_name}" №{self.order}: {self.question_text[:50]}'

class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer_options',
        verbose_name='Вопрос'
    )
    option_text = models.CharField(max_length=200, verbose_name='Текст варианта')
    is_correct = models.BooleanField(default=False, verbose_name='Правильность ответа')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок варианта')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.question} - {self.option_text} {"✓" if self.is_correct else "x"}'

class Story(models.Model):
    STORY_TYPE = [
        ('text', 'Текст'),
        ('image', 'Изображение'),
        ('video', 'Видео'),
    ]
    title = models.CharField(max_length=30)
    name = models.CharField(max_length=50,)
    story_type = models.CharField(
        max_length=10, choices=STORY_TYPE, default='text',verbose_name='Тип медиа'
    )
    content_video = models.FileField(
        upload_to='story_media/videos',
        validators=[FileExtensionValidator(
            allowed_extensions=[
                'mp4', 'mov', 'avi'
            ]
        )],
        verbose_name='Видео',
        blank=True,
        null=True,
    )
    content_image = models.ImageField(upload_to='story_media/photos')
    content_text = models.TextField(max_length=100,
                                    blank=True,
                                    null=True,
                                    default='Текст истории',
                                    help_text='Текст истории (можно оставить путсым)')
    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус истории',
        help_text='Определяет активна история для пользваотеля или нет'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    expires_at = models.DateTimeField(
        verbose_name='Дата истечения',
        help_text='Когда сторис автоматически станет неактивной'
    )
    class Meta:
        verbose_name = "История"
        verbose_name_plural = 'Истории'
        ordering = ['created_at']

    def clean(self):
        if self.story_type == 'image' and not self.content_image:
            raise ValidationError('Для типа "Изображение" необходимо загрузить изображение')
        if self.story_type == 'video' and not self.content_video:
            raise ValidationError('Для типа "Видео" необходимо загрузить видео')
        if self.story_type == 'text' and not self.content_text:
            raise ValidationError('Для типа "Текст" необходимо заполнить содержание')

    def __str__(self):
        return f'{self.name}, {self.created_at}-{self.expires_at}'