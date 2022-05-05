from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')



class EmailForm(forms.Form):
    name = forms.CharField()
    recipient = forms.EmailField()
    city = forms.CharField()
    address = forms.CharField()
    message = "Dear " + str(name) + " We have accepted your order, wait for your order at the following address: " + str(city)+" "+str(address)+". The courier will call you in advance."


# class NewProduct(forms.Form):
#     name = forms.CharField(max_length=200)
#     price = forms.FloatField()
#     image = forms.ImageField(null=True, blank=True)
#
