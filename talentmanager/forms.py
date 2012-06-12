from django import forms

EXCEL_MIMETYPES = set(['application/excel',
                       'application/vnd.ms-excel',
                       'application/x-excel',
                       'application/x-msexcel',
                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
                       

class GoogleDocForm(forms.Form):
    google_username = forms.CharField()
    google_password = forms.CharField(widget=forms.PasswordInput)
    document_name = forms.CharField()

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='')

    def clean(self):
        cleaned_data = super(ExcelUploadForm, self).clean()
        upl_file = cleaned_data.get('file')
        if not upl_file.content_type in EXCEL_MIMETYPES:
            raise forms.ValidationError('That doesn\'t look like an excel spreadsheet to me')
        return cleaned_data
