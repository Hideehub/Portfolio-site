from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot: hidden from people, but bots tend to fill every field.
    website = forms.CharField(required=False, label="Leave this field empty")

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Please enter your name.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write at least 10 characters.")
        return message

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
