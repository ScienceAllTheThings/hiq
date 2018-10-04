from django.db import models
from wagtail.core.models import Orderable, Page
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import InlinePanel
from django.utils.html import strip_tags

from django.contrib.auth.models import User

class SingleQuestion(models.Model):
    question = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    ans1 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    ans2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    ans3 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    ans4 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    ans5 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    POSSIBLE_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
        (5, 'E')
    )

    correct_ans = models.IntegerField(
        max_length=2,
        choices=POSSIBLE_CHOICES,
    )

    QUESTION_CATEGORIES = (
        ('logic', 'Logic'),
        ('math', 'Math'),
        ('pattern', 'Pattern'),
        ('spacial', 'Spacial'),
        ('language', 'Language'),
        ('reasoning', 'Reasoning'),

    )

    category = models.CharField(
        max_length=25,
        choices=QUESTION_CATEGORIES,
    )

    panels = [
        FieldPanel('question'),
        ImageChooserPanel('image'),
        FieldPanel('ans1'),
        FieldPanel('ans2'),
        FieldPanel('ans3'),
        FieldPanel('ans4'),
        FieldPanel('ans5'),
        FieldPanel('correct_ans'),
        FieldPanel('category'),
    ]

    @property
    def question_text(self):
        return strip_tags(self.question)

class AssessmentStartEnd(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    start_time = models.DateTimeField(
        auto_now_add=True,
    )

    end_time = models.DateTimeField(

    )


class AssessmentQuestionsPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        # TODO: make this so that it selects 50 random questions
        questions = SingleQuestion.objects.all()
        context['questions'] = questions
        return context

    def serve(self, request):
        if request.method == 'GET':
            
        return super().serve(request)
