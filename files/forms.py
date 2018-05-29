from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file.size > 1024*1024:
            raise forms.ValidationError("file too large (limit 10 byte)")
        else:
            return file


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_file_field(self):
        file_field = self.cleaned_data["file_field"]
        if file_field.size > 1024*1024:
            raise forms.ValidationError("files too large (limit 100 byte)")
        return file_field