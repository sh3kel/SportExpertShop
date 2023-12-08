from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'user@example.com',
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите адрес',
        'class': 'form-control'
    }))
    post_index = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '444444',
        'class': 'form-control'
    }))

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Промокод',
        'aria - label' : "Recipient's username",
        'aria - describedby' : "basic-addon2",
    }))