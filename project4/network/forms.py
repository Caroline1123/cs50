from django import forms

class PostForm(forms.Form):
    text = forms.CharField(label='',widget=forms.Textarea(attrs={"rows":3, "cols":150, "class":"form-control", "id":"text"}))
