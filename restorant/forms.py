from django import forms
import models

class SetTableForm(forms.ModelForm):
    class Meta:
        model = models.SetTable
        exclude = []
    # end class

    def clean(self):
        if self.instance.pk:
            self.instance.table.aviable = True
            self.instance.table.save()
        # end if
        clean = super(SetTableForm, self).clean()
        return clean
    # end def

    def save(self, commit=True):
        settable = super(SetTableForm, self).save(commit)
        settable.table.aviable = False
        settable.table.save()
        return settable
    # end def
# end class
