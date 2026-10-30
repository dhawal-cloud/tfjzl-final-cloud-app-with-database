from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, Question, Choice, Submission


@login_required
def submit(request, course_id):
    if request.method != 'POST':
        return redirect('onlinecourse:course_list')

    course = get_object_or_404(Course, id=course_id)
    submission = Submission.objects.create(
        student=request.user,
        exam=course
    )

    for question in course.questions.all():
        choice_id = request.POST.get(str(question.id))
        if choice_id:
            choice = get_object_or_404(
                Choice,
                id=choice_id,
                question=question
            )
            submission.choices.add(choice)

    return redirect(
        'onlinecourse:show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        student=request.user,
        exam=course
    )

    questions = course.questions.prefetch_related('choices').all()
    total_questions = questions.count()
    score = 0

    for question in questions:
        correct_choices = question.choices.filter(is_correct=True)
        selected_choices = submission.choices.filter(
            question=question
        )

        if correct_choices.exists() and set(
            correct_choices.values_list('id', flat=True)
        ) == set(selected_choices.values_list('id', flat=True)):
            score += 1

    context = {
        'course': course,
        'submission': submission,
        'questions': questions,
        'score': score,
        'total_questions': total_questions,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
