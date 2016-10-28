# -*- coding: utf-8 -*-

from django.views import generic
from application.pricing.PricingApplicationService import PricingApplicationService
from django import template
from django import shortcuts

from .forms import EnterpriseForm
from infrastructure.pricing.mailer import PricingMailer

register = template.Library()


class IndexView(generic.ListView):
    service = PricingApplicationService()

    context_object_name = 'result'

    def get_queryset(self):
        return self.service.getFakeData()


def enterprise_upgrade(request):
    if request.method == 'POST':
        form = EnterpriseForm(request.POST)

        name = request.user.name + ' ' + request.user.surname
        email = request.user.email
        country_code = request.POST['country_code']
        phone = request.POST['phone']
        company = request.POST['company']
        company_website = request.POST['company_website']
        company_type = request.POST['company_type']
        number_location = request.POST['number_location']
        employee = request.POST['employee']
        software = request.POST['software']
        role = request.POST['role']
        content = request.POST['message']
        to_email = str(request.user)

        message = 'Name: %s\n' \
                  'Email: %s\n' \
                  'Phone: %s %s\n' \
                  'Company: %s\n' \
                  'Company website: %s\n' \
                  'Company type: %s\n' \
                  'Number of location: %s\n' \
                  'How many employees: %s\n' \
                  'What current recipe software do you use: %s\n' \
                  'What is your role: %s\n' \
                  'Comments:\n' \
                  '%s' % (
                      name, email, country_code, phone, company, company_website, company_type, number_location, employee, software,
                      role, content)

        if form.is_valid():
            try:
                pricing_mailer = PricingMailer.new()
                pricing_mailer.contact_about_enterprise(message, to_email)
                return redirect_to_homepage()
            except:
                print 'Unable to send email'
    else:
        form = EnterpriseForm()

    return shortcuts.render(request, 'pricing/enterprise_upgrade.html', {'form': form})


def redirect_to_homepage():
    return shortcuts.redirect('/')
