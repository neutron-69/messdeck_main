from django import forms
from .models import Feedbacks,rating_model

class Feedback_form(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['feed_back','picture']


class Rating_Form(forms.ModelForm):
    class Meta:
        model = rating_model
        fields = ['food_item','rating']