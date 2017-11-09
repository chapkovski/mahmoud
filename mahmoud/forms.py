import floppyforms.__future__ as forms
from .models import Q1, Q3, Player, Constants

from django.forms import inlineformset_factory, BaseFormSet, BaseInlineFormSet
import django.forms as djforms


class Q1Form(forms.ModelForm):
    class Meta:
        model = Q1
        fields = ['d1', 'd2']

    def clean(self):
        cleaned_data = super().clean()
        d1 = cleaned_data.get('d1')
        d2 = cleaned_data.get('d2')
        if d1 and d2:
            if d1 + d2 != Constants.q1endowment:
                raise forms.ValidationError(
                    "The total amount should equal {}".format(Constants.q1endowment)
                )
        return super().clean()


class Q3Form(forms.ModelForm):
    CHOICES = ((True, 'Option A',), (False, 'Option B',))
    answer = djforms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        curinstance = kwargs['instance']
        answer_choices= self.fields['answer'].widget.choices.copy()
        print(answer_choices)

        answer_choices[0] = (True, '{}: {}'.format(answer_choices[0][1], curinstance.option_a))
        answer_choices[1] = (False, '{}: {}'.format(answer_choices[1][1], curinstance.option_b))
        print(answer_choices)
        self.fields['answer'].widget.choices = answer_choices
        # print(curinstance.option_a)


Q1FormSet = inlineformset_factory(Player, Q1,
                                  can_delete=False,
                                  extra=0,
                                  form=Q1Form,
                                  formset=BaseInlineFormSet)

Q3FormSet = inlineformset_factory(Player, Q3,
                                  fields=['answer'],
                                  can_delete=False,
                                  extra=0,
                                  form=Q3Form,
                                  formset=BaseInlineFormSet)
