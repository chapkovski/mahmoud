from otree import __version__
if int(__version__.split('.')[0])<=1:
    import floppyforms.__future__ as forms
else:
    from django import forms



class EmailLookupForm(forms.Form):
    def __init__(self,  *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email']=forms.EmailField()
