from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
    # image = forms.ImageField(required=False)
    # title = forms.CharField(max_length=256)
    # content = forms.CharField(max_length=512)
        model = Post
        fields = ["image", "title", "content", "category"]

    def clean_title(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title and title.lower == "python":
            raise forms.ValidationError("Title cannot be python")
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if (title == content) or (title.lower() == content.lower()):
            raise forms.ValidationError("title and content cannot be same")
        return cleaned_data
    
class SearchForm(forms.Form):
    search = forms.CharField(max_length=80, required=False)
    category_id = forms.ModelChoiceField (queryset=Category.objects.all(), required=False)

    orderings = (
        ("created_at", "Creation Date (asc)"),
        ("-created_at", "Creation Date (desc)"),
        ("rate", "Rate"),
        ("-rate", "Rate (desc)"),
    )
    ordering = forms.ChoiceField(choices=orderings, required=False)