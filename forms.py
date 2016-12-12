from wagtail.wagtailadmin.forms import WagtailAdminModelForm

class ProductAdminModelForm(WagtailAdminModelForm):
    def clean_ean(self):
        if self.cleaned_data['ean'] == '':
            self.cleaned_data['ean'] =  None

        return self.cleaned_data['ean']

    def clean_sku(self):
        if self.cleaned_data['sku'] == '':
            self.cleaned_data['sku'] =  None

        return self.cleaned_data['sku']
        
