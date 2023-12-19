from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

    def save(self, commit=True, user=None):
        """
        Save the form and set the user before saving to the database.
        """
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance