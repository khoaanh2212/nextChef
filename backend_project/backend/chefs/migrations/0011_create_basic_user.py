# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from chefs.models import Chefs
import os


class Migration(DataMigration):

    def forwards(self, orm):
        ##create dev super user ##
        devSuperUser = self.checkUserExists('developer-1@apiumtech.com')
        if not devSuperUser:
            devSuperUser = Chefs.objects.create_superuser(email='developer-1@apiumtech.com',password='7c079899d8',
                                                      name='admin',surname='Admin')
        else:
            self.updateSuperUser(devSuperUser, 'admin', '7c079899d8')

        ##create client super user ##
        clientSuperUser = self.checkUserExists('admin@nextchef.co')
        if not clientSuperUser:
            clientSuperUser = Chefs.objects.create_superuser(email='admin@nextchef.co', name='chef', surname='Chef',
                                                             password='4f87e4a2ef')
        else:
            self.updateSuperUser(clientSuperUser, 'chef', '4f87e4a2ef')

        ##create dev enterprise user for test##
        enterpriseUser = self.checkUserExists('dev@apiumtech.com')
        if not enterpriseUser:
            enterpriseUser = Chefs.objects.create_user(email='dev@apiumtech.com', password='a9a92707d',
                                                       name='enterprise',
                                                       surname='EnterPrise')
        else:
            enterpriseUser.name = 'enterprise'
            enterpriseUser.set_password('a9a92707d')
            enterpriseUser.save()
        enterpriseUser.membership = 'enterprise'
        enterpriseUser.save()

    def backwards(self, orm):
        raise RuntimeError("Can't go backwards")

    def checkUserExists(self, email):
        try:
            return Chefs.objects.get(email=email)
        except:
            return False

    def updateSuperUser(self, user, name='test', password='123456'):
        user.is_superuser = True
        user.is_staff = True
        user.is_confirmed = True
        user.name = name
        user.set_password(password)
        user.save()
