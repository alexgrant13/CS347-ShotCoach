from django import forms

from .models import Shot


class ShotForm(forms.ModelForm):
    class Meta:
        model = Shot
        fields = ["image", "title", "idea_text"]
        labels = {"idea_text": "What were you going for? (optional)"}
        widgets = {
            "idea_text": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Moody, cinematic portrait under neon signs"}
            ),
        }
