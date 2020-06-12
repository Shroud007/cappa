import json
from django.core.cache import cache
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from src.langs.models import Lang
from src.utils.fields import OrderField


UserModel = get_user_model()


class Quiz(models.Model):
    class Meta:
        verbose_name = "Самостоятельная работа"
        verbose_name_plural = "самостоятельные работы"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255, unique=True)
    lang = models.ForeignKey(Lang, verbose_name="язык программирования")
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    end_time = models.DateTimeField(
        verbose_name="дата/время окончения решения задач в формате UTC",
        blank=True, null=True
    )
    about = HTMLField(verbose_name="краткое описание", default="", blank=True, null=True)
    content = HTMLField(verbose_name="текстовый контент", default="", blank=True, null=True)


    order_key = OrderField(verbose_name='порядок', blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    
    
    
    @property
    def taskitems(self):
        return self._taskitems.filter(show=True)

    @property
    def cache_key(self):
        return 'quiz__%d' % self.id

    def get_data(self):
        return {
            'id': self.cache_key,
            'title': self.title,
            'url': reverse('quizzes:quiz', kwargs={'quiz': self.slug}), 
            'taskitems': [taskitem.get_data() for taskitem in self.taskitems],
        }

    def get_cache_data(self):
        json_data = cache.get(self.cache_key)
        if not json_data:
            data = self.get_data()
            cache.set(self.cache_key, json.dumps(data, ensure_ascii=False))
        else:
            data = json.loads(json_data)
        return data

    def get_breadcrumbs(self):
        return [
            {'title': 'Работы', 'url': reverse('quizzes:quizzes')},
        ]

    def get_absolute_url(self):
        return self.get_cache_data()['url']

    def __str__(self):
        return self.title