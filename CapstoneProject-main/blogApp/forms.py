from django import forms
from .models import Post,Comment,Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_id','title','article','post_image','video','ppt','Notes','link','youtube_link')
    post_image = forms.ImageField(required=True)
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {"body":"Comment Section:"}

        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Enter Your Comment"}),
        }
  

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)
        labels ={"reply_body":"Reply Here :"}
        widgets = {
            'reply_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':6, 'placeholder':"Enter Your Reply"}),
        }
   