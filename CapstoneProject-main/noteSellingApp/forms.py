from django import forms
from .models import Lesson,Review

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_id','name','description','image1','image2','image3','lesson_video','Notes')
    image1 = forms.ImageField(required=True)
    image2 = forms.ImageField(required=True)
    image3 = forms.ImageField(required=True)
    Notes = forms.FileField(required=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)

        labels = {"body":"Review Comment:"}

        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Enter Your Feedback"}),
        }

