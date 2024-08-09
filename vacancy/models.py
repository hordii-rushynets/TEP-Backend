from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField


class Name(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)


class ScopeOfWork(Name):
    """ScopeOfWork Model"""


class TypeOfWork(Name):
    """TypeOfWork Model"""


class TypeOfEmployment(Name):
    """TypeOfEmployment Model"""


class Tag(Name):
    """Tag Model"""


class Address(models.Model):
    """Address Model"""
    city = models.CharField(max_length=128, default=None)
    region = models.CharField(max_length=128, default=None)

    def __str__(self):
        return f'{self.region} {self.city}'


class Vacancy(models.Model):
    """Vacancy Model"""
    image = models.ImageField(upload_to='vacancy/images/', blank=True)

    title = models.CharField(max_length=128)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='vacancy')

    description = RichTextField(max_length=30000)
    about_company = RichTextField(max_length=30000)

    scope_of_work = models.ManyToManyField(ScopeOfWork)
    type_of_work = models.ManyToManyField(TypeOfWork)
    type_of_employment = models.ManyToManyField(TypeOfEmployment)
    tag = models.ManyToManyField(Tag)

    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)


class CooperationOffer(models.Model):
    """Cooperation Offer Model"""
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='response_to_a_vacancy', null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = RichTextField(max_length=30000, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class CooperationOfferFile(models.Model):
    """Cooperation Offer file Model"""
    file = models.FileField(upload_to='cooperation_offer/files/', blank=True)
    cooperation_offer = models.ForeignKey(CooperationOffer, on_delete=models.CASCADE,
                                          related_name='cooperation_offer_files', null=True)
