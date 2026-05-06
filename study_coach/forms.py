from django import forms

from core.models import Document


class QuizGeneratorForm(forms.Form):
    LEVEL_CHOICES = [
        ("basic", "Basic"),
        ("intermediate", "Intermediate"),
    ]

    document = forms.ModelChoiceField(
        queryset=Document.objects.none(),
        empty_label="Select a document",
    )
    level = forms.ChoiceField(choices=LEVEL_CHOICES, initial="basic")
    question_count = forms.IntegerField(min_value=3, max_value=10, initial=5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["document"].queryset = Document.objects.order_by("-created_at")
        shared_classes = "w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition focus:border-cyan-400"
        self.fields["document"].widget.attrs.update({"class": shared_classes})
        self.fields["level"].widget.attrs.update({"class": shared_classes})
        self.fields["question_count"].widget.attrs.update({"class": shared_classes})
