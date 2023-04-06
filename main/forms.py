
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms


class ContactForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
