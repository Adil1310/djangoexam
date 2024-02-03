from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
			'title', 
			'category',
			'body', 
			'image',
		]
        widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
			'category': forms.TextInput(attrs={'class': 'form-control' , 'required': 'True'}),
			'body': forms.Textarea(attrs={'class': 'form-control' , 'required': 'True'}),
			'image': forms.FileInput(attrs={'class': 'form-control'}),
		}