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
    message = "Уважаемый " + str(name) + " Мы приняли ваш заказ, ожидайте свой заказ, по следующему указанному адресу: " + str(city)+" "+str(address)+". Курьер  заранее вам позванит."


# class NewProduct(forms.Form):
#     name = forms.CharField(max_length=200)
#     price = forms.FloatField()
#     image = forms.ImageField(null=True, blank=True)
#
