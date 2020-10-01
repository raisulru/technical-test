#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum


class Company(models.Model):
    name = models.CharField(max_length=150)
    bic = models.CharField(max_length=150, blank=True)

    def get_order_count(self):
        return self.orders.count()

    def get_order_sum(self):
        contact_id_list = self.contacts.all().values_list('id', flat=True)
        total = Order.objects.filter(contact_id__in=contact_id_list).aggregate(Sum('total')).get('total__sum', 0)
        return total
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    company = models.ForeignKey(
        Company, related_name="contacts", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()

    def get_order_count(self):
        return self.orders.count()
    
    def __str__(self):
        return self.email


class Order(models.Model):
    order_number = models.CharField(max_length=150)
    company = models.ForeignKey(Company, related_name="orders", on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, related_name="orders", on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=18, decimal_places=9)
    order_date = models.DateTimeField(null=True, blank=True)
    # for internal use only
    added_date = models.DateTimeField(auto_now_add=True)
    # for internal use only
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.order_number
