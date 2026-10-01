from django import forms

from .models import Resource, Topic


# A ModelForm builds its fields from the model, so we don't repeat ourselves.
# It also validates the input (e.g. title not empty, URL looks like a URL).
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        # owner is NOT listed: the view sets it to the logged-in user,
        # so nobody can create topics for someone else.
        fields = ["title", "description", "status"]
        widgets = {
            # Make the description box a bit taller than the default
            "description": forms.Textarea(attrs={"rows": 5}),
        }
        help_texts = {
            "description": "Optional. What it covers, or notes to yourself.",
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "url"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Django tutorial part 1"}),
            "url": forms.URLInput(attrs={"placeholder": "https://…"}),
        }
