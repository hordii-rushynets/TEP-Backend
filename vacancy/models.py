from django.db import models


class ScopeOfWork(models.Model):
    """ScopeOfWork Model"""
    name = models.CharField()

    def __str__(self):
        return str(self.name)


class TypeOfWork(models.Model):
    """TypeOfWork Model"""
    name = models.CharField()

    def __str__(self):
        return str(self.name)


class TypeOfEmployment(models.Model):
    """TypeOfEmployment Model"""
    name = models.CharField()

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    """Tag Model"""
    name = models.CharField()

    def __str__(self):
        return str(self.name)


class Vacancy(models.Model):
    """Vacancy Model"""
    image = models.ImageField(upload_to='vacancy/images/', blank=True)

    title = models.CharField(max_length=128)
    city = models.CharField(max_length=128, default=None)
    region = models.CharField(max_length=128, default=None)

    description = models.TextField()
    about_company = models.TextField()

    scope_of_work = models.ManyToManyField(ScopeOfWork)
    type_of_work = models.ManyToManyField(TypeOfWork)
    type_of_employment = models.ManyToManyField(TypeOfEmployment)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.title)
