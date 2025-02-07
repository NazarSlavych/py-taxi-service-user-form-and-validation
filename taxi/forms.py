import re
from django.contrib.auth.forms import UserCreationForm
from django import forms
from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField(
        max_length=8, min_length=8, required=True, label="License Number"
    )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        # Перевірка формату ліцензії за допомогою регулярного виразу
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must have 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_form = DriverLicenseUpdateForm(self.data)
        if license_form.is_valid():
            return license_form.cleaned_data["license_number"]

        # Додати перше доступне повідомлення про помилку
        error_message = license_form.errors.get("license_number", ["Invalid license number"])[0]
        self.add_error("license_number", error_message)
        raise forms.ValidationError("Wrong license number.")


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
