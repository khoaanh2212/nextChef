from django.core.management import call_command

import bootstrap


def start_server(name, setting, *args, **options):
    if 'runserver' == name:
        bootstrap.init(setting)
        call_command(name, *args, **options)
    else:
        bootstrap.set_module_env_settings(setting)
        if 'develop' == name:
            call_command('runserver', *args, **options)
        else:
            call_command(name, *args, **options)
