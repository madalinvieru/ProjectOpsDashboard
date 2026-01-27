from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=255
    )

    description = forms.CharField(
        required=False
    )

    location = forms.CharField(
        required=False,
        max_length=500
    )

    type = forms.CharField(
        required=False,
        max_length=100
    )

    start_date = forms.DateTimeField(
        required=False
    )

    end_date = forms.DateTimeField(
        required=False
    )

    status = forms.ChoiceField(
        required=False
    )

    reason = forms.CharField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        project_status = kwargs.pop('project_status', [])

        super().__init__(*args, **kwargs)

        self.fields['status'].choices = project_status