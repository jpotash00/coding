from django import forms
class SearchORInsert(forms.Form):
    song_title = forms.CharField(help_text="Enter a Song", required=True)

    # def clean_title(self):
    #     data = self.cleaned_data['song']

    #     # Check if a date is not in the past.
    #     if data < datetime.date.today():
    #         raise ValidationError(_('Invalid date - renewal in past'))

    #     # Check if a date is in the allowed range (+4 weeks from today).
    #     if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #         raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

    #     # Remember to always return the cleaned data.
    #     return data