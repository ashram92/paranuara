from django.db import models


class Company(models.Model):
    """A company on the planet of Paranuara"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return '<{}: {}>'.format(self.name, self.id)
