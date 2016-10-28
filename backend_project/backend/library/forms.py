from django import forms

from chefs.models import Chefs, Restaurant


class EditChefForm(forms.ModelForm):
    class Meta:
        model = Chefs
        fields = ['name', 'surname', 'web', 'location', 'short_bio', 'description', 'email_newsletter',
                  'email_notifications', 'email', 'facebook_page', 'twitter_page', 'linkedin_page', 'instagram_page',
                  'pinterest_page']

    def __init__(self, *args, **kwargs):
        super(EditChefForm, self).__init__(*args, **kwargs)
        self.fields['short_bio'].widget = forms.TextInput(attrs={'maxlength': 70})


class EditRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'type', 'address', 'phone', 'zip', 'city', 'state', 'country', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(EditRestaurantForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['city'].widget = forms.HiddenInput()
        self.fields['zip'].widget = forms.HiddenInput()
        self.fields['state'].widget = forms.HiddenInput()
        self.fields['country'].widget = forms.HiddenInput()
        self.fields['name'].label = "Company"
        self.fields['phone'].label = "Telephone"
        self.fields['address'].widget.attrs['placeholder'] = "Street and number, Zip, City"

    def clean(self):
        cleaned_data = super(EditRestaurantForm, self).clean()
        return cleaned_data


class EditSocialForm(forms.ModelForm):
    class Meta:
        model = Chefs
        fields = ['facebook_page', 'twitter_page', 'linkedin_page', 'instagram_page', 'pinterest_page']

    def __init__(self, *args, **kwargs):
        super(EditSocialForm, self).__init__(*args, **kwargs)
        self.fields['facebook_page'].label = "Facebook"
        self.fields['twitter_page'].label = "Twitter"
        self.fields['linkedin_page'].label = "Linkedin"
        self.fields['instagram_page'].label = "Instagram"
        self.fields['pinterest_page'].label = "Pinterest"

    def clean(self):
        cleaned_data = super(EditSocialForm, self).clean()
        for key in cleaned_data:
            value = cleaned_data[key]
            if "http://" in value:
                cleaned_data[key] = value.replace('http://', '')
            elif "https://" in value:
                cleaned_data[key] = value.replace('https://', '')
        if cleaned_data['twitter_page'].startswith('@'):
            cleaned_data['twitter_page'] = cleaned_data['twitter_page'].replace('@', 'twitter.com/')
        return cleaned_data
