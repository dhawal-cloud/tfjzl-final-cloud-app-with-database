from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Question(models.Model):
    course = models.ForeignKey(
        'onlinecourse.Course',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)  # points for this question

    def __str__(self):
        return "Question: " + self.question_text

    # Returns True only if the learner selected ALL correct choices
    # and NONE of the incorrect ones
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(
            is_correct=True, id__in=selected_ids
        ).count()
        selected_total = self.choice_set.filter(id__in=selected_ids).count()
        return all_answers == selected_correct and selected_correct == selected_total


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        'onlinecourse.Enrollment',
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return "Submission " + str(self.id)
