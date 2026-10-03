from django import forms

from .models import ContactSubmission, NewsletterSignup, Testimony


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ["first_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = [
            "topic",
            "name",
            "email",
            "phone",
            "organization",
            "event_type",
            "event_date",
            "location",
            "message",
        ]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }


class InviteForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = [
            "name",
            "organization",
            "email",
            "phone",
            "event_type",
            "event_date",
            "location",
            "message",
        ]
        labels = {
            "organization": "Organization / Church",
            "event_type": "Event type",
            "event_date": "Event date",
        }
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.topic = "speaking"
        if commit:
            obj.save()
        return obj


class TestimonyForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Testimony
        fields = ["name", "location", "title", "story", "photo", "video_url", "category", "consent_given"]
        widgets = {
            "story": forms.Textarea(attrs={"rows": 6, "placeholder": "Share what God has done..."}),
            "title": forms.TextInput(attrs={"placeholder": "Short headline for your story"}),
            "location": forms.TextInput(attrs={"placeholder": "City, Country"}),
            "video_url": forms.URLInput(attrs={"placeholder": "Optional YouTube link"}),
        }

    def clean_honeypot(self):
        if self.cleaned_data.get("honeypot"):
            raise forms.ValidationError("Invalid submission.")
        return ""

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if not photo:
            return photo

        allowed_types = {"image/jpeg", "image/png", "image/webp"}
        if photo.content_type not in allowed_types:
            raise forms.ValidationError("Please upload a JPG, PNG or WebP image.")
        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image must be 5MB or smaller.")
        return photo

    def save(self, commit=True):
        testimony = super().save(commit=False)
        testimony.is_published = False
        testimony.is_approved = False
        if commit:
            testimony.save()
        return testimony
