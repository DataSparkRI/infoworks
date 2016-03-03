from django import forms
from django.utils.translation import ugettext_lazy as _
from data.models import StateDisplayDataY, DistrictDisplayDataY, SchoolDisplayDataY

class StateDisplayDataYForm(forms.ModelForm):
    display = forms.ChoiceField(label=_('Display'), required=False, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
       model = StateDisplayDataY
       fields = ('display','order')

    def __init__(self, *args, **kwargs):
       super(StateDisplayDataYForm, self).__init__(*args, **kwargs)

class DistrictDisplayDataYForm(forms.ModelForm):
    display = forms.ChoiceField(label=_('Display'), required=False, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
       model = DistrictDisplayDataY
       fields = ('display','order')

    def __init__(self, *args, **kwargs):
       super(DistrictDisplayDataYForm, self).__init__(*args, **kwargs)


class SchoolDisplayDataYForm(forms.ModelForm):
    display = forms.ChoiceField(label=_('Display'), required=False, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
       model = SchoolDisplayDataY
       fields = ('display','order')

    def __init__(self, *args, **kwargs):
       super(SchoolDisplayDataYForm, self).__init__(*args, **kwargs)
       #topic_types = self.school_indicator.dataset
       #self.fields['display'].choices = [(tp.id, tp.name) for tp in topic_types]
       MY_CHOICES = (
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
       )
       self.fields['display'].choices = MY_CHOICES

