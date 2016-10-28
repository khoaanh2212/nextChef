from behave import *

use_step_matcher("re")


@given("The system now have 100 recipes")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I input (?P<page>.+) into browser address bar")
def step_impl(context, page):
    """
    :type context: behave.runner.Context
    :type page: str
    """
    pass


@then("I will see first (?P<num>.+) recipes in the page")
def step_impl(context, num):
    """
    :type context: behave.runner.Context
    :type num: str
    """
    pass


@given("I input (?P<page>.+) into browser address bar")
def step_impl(context, page):
    """
    :type context: behave.runner.Context
    :type page: str
    """
    pass


@step("I click on the login link")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I Input username: (?P<username>.+) and password: (?P<password>.+)")
def step_impl(context, username, password):
    """
    :type context: behave.runner.Context
    :type username: str
    :type password: str
    """
    pass


@when("I click on the sign in button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('I will see the error message: "(?P<error_message>.+)"')
def step_impl(context, error_message):
    """
    :type context: behave.runner.Context
    :type error_message: str
    """
    pass