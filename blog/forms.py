from django import forms

class CommentForm(forms.Form):
    description = forms.Textarea()
    

