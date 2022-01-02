# Create your tests here.
from django.test import TestCase
from django.test import Client
from .models import Manager, Org
from django.db import models
from django.utils import timezone

# Create your tests here.

class OrgTestCase(TestCase):
    def setUp(self):
        self.email = 'yinzc18@mails.tsinghua.edu.cn'
        self.name = 'ABC社'
        self.description = 'ABC社团是ABC社团'

    def test_model(self):
        Org.objects.create(email=self.email, name=self.name, description=self.description)
        org = Org.objects.filter(email = self.email)
        org = org[0]
        self.assertEqual(org.email, self.email)
        self.assertEqual(org.name, self.name)
        self.assertEqual(org.description, self.description)