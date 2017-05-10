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


class BuySupplyForm(forms.ModelForm):
    class Meta:
        model = models.BuySupply
        exclude = []
    # end class

    def save(self, commit=True):
        obj = super(BuySupplyForm, self).save(commit=False)
        obj.current_count = obj.buy_count
        obj.save()
        return obj
    # end def
# end class

class SupplyRequestForm(forms.ModelForm):

    class Meta:
        model = models.SupplyRequest
        exclude = ["service"]
    #end class

    def save(self, commit = True):
        pedidoSuministro = super(SupplyRequestForm, self).save(commit)
        usuario = CuserMiddleware.get_user()
        pedidoSuministro.service = models.Service.objects.filter(userservice__user = usuario).first()
        pedidoSuministro.save()
        return pedidoSuministro
    #end def

#end class

class SupplyForm(forms.ModelForm):
    class Meta:
        model = models.Supply
        exclude = ["service"]
    #end class

    def save(self, commit = True):
        suministro = super(SupplyForm, self).save(commit)
        usuario = CuserMiddleware.get_user()
        suministro.service = models.Service.objects.filter(userservice__user = usuario).first()
        suministro.save
        return suministro
    #end def
#end class