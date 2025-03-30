from django import forms
from .models import Plant, Comment
from taggit.managers import TaggableManager
from taggit.forms import TagField

class PlantFilterForm(forms.Form):
    light = forms.CharField(required=False)
    moisture = forms.CharField(required=False)
    form = forms.CharField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.user and self.user.is_authenticated:
            comment.user_profile = self.user.profile
        if commit:
            comment.save()
        return comment
    

class TagForm(forms.Form):
    tags = TagField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


    