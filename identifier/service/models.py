from django.db import models


SIZE_OF_PART_NAME = 65
SIZE_OF_PASSPORT_NUMBER = 6
SIZE_OF_PASSPORT_SERIES = 4


class SimpleWords(models.Model):
    value = models.CharField(max_length=SIZE_OF_PART_NAME, primary_key=True, unique=True)


class IdentifiablePerson(models.Model):
    id = models.AutoField(primary_key=True)
    passport_series = models.CharField(max_length=SIZE_OF_PASSPORT_SERIES)
    passport_number = models.CharField(max_length=SIZE_OF_PASSPORT_NUMBER)
    first_name = models.CharField(max_length=SIZE_OF_PART_NAME)
    middle_name = models.CharField(max_length=SIZE_OF_PART_NAME)
    last_name = models.CharField(max_length=SIZE_OF_PART_NAME)
    birthday = models.DateField()


class IdentificationAttempt(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(IdentifiablePerson, on_delete=models.CASCADE)
    response = models.BooleanField()
    attempt_date = models.DateTimeField(auto_now_add=True)


class BadPassports(models.Model):
    id = models.AutoField(primary_key=True)
    passport_series = models.CharField(max_length=SIZE_OF_PASSPORT_SERIES)
    passport_number = models.CharField(max_length=SIZE_OF_PASSPORT_NUMBER)
