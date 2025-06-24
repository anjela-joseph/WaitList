from django import forms

class WaitlistForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=100)
    contact = forms.CharField(label="Contact Number", max_length=15)
    email = forms.EmailField(label="Your Email")
    course = forms.ChoiceField(
        label="Select Course",
        choices=[
            ('student', 'Student'),
            ('employee', 'Employee'),
            ('executive', 'Executive'),
        ]
    )
