from django import forms


class FileUploadForm(forms.Form):
    """File upload form."""
    excelfile = forms.FileField(required=True)