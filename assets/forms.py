from django import forms
from .models import Asset, AssetMovement, MaintenanceRecord

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name', 'category', 'serial_number', 'department', 'assigned_to',
            'purchase_date', 'condition', 'status', 'description'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MovementForm(forms.ModelForm):
    class Meta:
        model = AssetMovement
        fields = ['asset', 'from_department', 'to_department', 'remarks']


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['asset', 'issue_reported', 'maintenance_date', 'performed_by', 'remarks']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }
