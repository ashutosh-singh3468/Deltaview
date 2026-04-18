from django import forms


class DocumentCompareForm(forms.Form):
    left_file = forms.FileField(label='Left Document')
    right_file = forms.FileField(label='Right Document')

    def clean(self):
        cleaned_data = super().clean()
        allowed_extensions = {'pdf', 'docx', 'txt'}
        for field in ('left_file', 'right_file'):
            uploaded = cleaned_data.get(field)
            if uploaded:
                ext = uploaded.name.rsplit('.', 1)[-1].lower() if '.' in uploaded.name else ''
                if ext not in allowed_extensions:
                    self.add_error(field, 'Only PDF, DOCX, and TXT files are allowed.')
        return cleaned_data
