from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your full name",
                "autocomplete": "name",
                "data-required": "true",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "data-required": "true",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "+254 7XX XXX XXX (optional)",
                "autocomplete": "tel",
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "What can we help with?",
                "data-required": "true",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Tell us about the occasion, flowers you love, or any questions you have...",
                "rows": 6,
                "data-required": "true",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please tell us a bit more (at least 10 characters).")
        return message
