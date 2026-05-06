from django.shortcuts import render

from .forms import QuizGeneratorForm
from .services import QuizGenerationError, generate_quiz_for_document


def generate_quiz(request):
    initial = {}
    document_id = request.GET.get("document_id")
    if document_id:
        initial["document"] = document_id

    quiz = None
    error_message = None

    if request.method == "POST":
        form = QuizGeneratorForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data["document"]
            level = form.cleaned_data["level"]
            question_count = form.cleaned_data["question_count"]
            try:
                quiz = generate_quiz_for_document(document, level, question_count)
            except QuizGenerationError as exc:
                error_message = str(exc)
    else:
        form = QuizGeneratorForm(initial=initial)

    return render(
        request,
        "study_coach/generate_quiz.html",
        {
            "form": form,
            "quiz": quiz,
            "error_message": error_message,
        },
    )
