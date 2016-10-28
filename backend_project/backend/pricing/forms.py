from django import forms


class EnterpriseForm(forms.Form):
    COMPANY_TYPE = [
        ('', '-- Please choose --'),
        ('Artisan', 'Artisan'),
        ('Bar, Cocktai Bar', 'Bar, Cocktai Bar'),
        ('Chef', 'Chef'),
        ('Chef, consultant', 'Chef, consultant'),
        ('Chef, personal', 'Chef, personal'),
        ('Food or Drink Brand', 'Food or Drink Brand'),
        ('Food producer', 'Food producer'),
        ('Food stylist', 'Food stylist'),
        ('Hotel', 'Hotel'),
        ('R & D', 'R & D'),
        ('Pub', 'Pub'),
        ('Restaurant', 'Restaurant'),
        ('School or University', 'School or University'),
        ('Supplier', 'Supplier'),
        ('Take away', 'Take away'),
        ('University', 'University')
    ]
    NUMBER_LOCATION = [
        ('', '-- Please choose --'),
        ('Single location', 'Single location'),
        ('2-10', '2-10'),
        ('11-25', '11-25'),
        ('26', '26'),
        ('100', '100'),
        ('100+', '100+')
    ]
    EMPLOYEE = [
        ('', '-- Please choose --'),
        ('1', '1'),
        ('2-5', '2-5'),
        ('6-10', '6-10'),
        ('11-25', '11-25'),
        ('26-50', '26-50'),
        ('51-200', '51-200'),
        ('201-1,000', '201-1,000'),
        ('1,100-10,000', '1,100-10,000'),
        ('1,001 or more', '1,001 or more')
    ]
    SOFTWARE = [
        ('', '-- Please choose --'),
        ('Agilysys', 'Agilysys'),
        ('Bim POS', 'Bim POS'),
        ('Calc menu', 'Calc menu'),
        ('Chefs control', 'Chefs control'),
        ('Cook\'n Recipe Organizer', 'Cook\'n Recipe Organizer'),
        ('Cost Guard', 'Cost Guard'),
        ('Cuiner', 'Cuiner'),
        ('Dietary Manager', 'Dietary Manager'),
        ('EGS Cals Menu', 'EGS Cals Menu'),
        ('eZee', 'eZee'),
        ('Mastercook', 'Mastercook'),
        ('Mirus', 'Mirus'),
        ('Myechef', 'Myechef'),
        ('Oracle micros', 'Oracle micros'),
        ('Parika', 'Parika'),
        ('Simple Order', 'Simple Order'),
        ('True Restaurant Managerment', 'True Restaurant Managerment'),
        ('tspoonlab', 'tspoonlab'),
        ('Other (specify)', 'Other (specify)')
    ]
    ROLE = [
        ('', '-- Please choose --'),
        ('C-Lever/ Owner', 'C-Lever/ Owner'),
        ('VP/ Director', 'VP/ Director'),
        ('Manager', 'Manager'),
        ('Individual Contributor', 'Individual Contributor'),
        ('Student/ Intern', 'Student/ Intern'),
        ('Other', 'Other'),
    ]

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone',
                'style': 'width: 100%'
            }
        )
    )
    company = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Company',
                'style': 'width: 100%'
            }
        )
    )
    company_website = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Company Website',
                'style': 'width: 100%'
            }
        )
    )
    company_type = forms.ChoiceField(
        choices=COMPANY_TYPE,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    number_location = forms.ChoiceField(
        choices=NUMBER_LOCATION,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    employee = forms.ChoiceField(
        choices=EMPLOYEE,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    software = forms.ChoiceField(
        choices=SOFTWARE,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=ROLE,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Comments',
                'col': '30',
                'rows': '10'
            }
        ),
        required=False
    )
