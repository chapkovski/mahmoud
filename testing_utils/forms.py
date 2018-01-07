import floppyforms as forms




class EmailLookupForm(forms.Form):
    def __init__(self,  *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email']=forms.EmailField()
