from django import forms
from accounts.models import User
from .models import Project

# ==============================
# ======== PROJECT FORM ========
# ==============================
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

# ===========================
# ======== TASK FORM ========
# ===========================
class TaskForm(forms.Form):
    title = forms.CharField(
        required=True,
        max_length=255
    )

    description = forms.CharField(
        required=False
    )

    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False
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

    priority = forms.ChoiceField(
        required=False
    )

    parent = forms.IntegerField(
        required=False
    )

    created_by = forms.IntegerField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', 0)
        task_status = kwargs.pop('task_status', [])
        task_priority = kwargs.pop('task_priority', [])

        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = User.objects.filter(id=user_id)
        self.fields['status'].choices = task_status
        self.fields['priority'].choices = task_priority

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'End date cannot be earlier than start date.'
            )

        return cleaned_data