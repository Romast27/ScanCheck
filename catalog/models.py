from django.db import models
import uuid
from django.contrib.auth.models import User


class Barcodes(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    id = models.IntegerField(primary_key=True)
    barcode = models.IntegerField(unique=True)
    name_product = models.TextField(max_length=1500, help_text='Enter a name of product', null=True)
    category_name = models.TextField(max_length=500, help_text="Enter a name of product's category", null=True)
    brand_name = models.TextField(max_length=250, help_text="Enter a name of product's brand", null=True)

    class Meta:
        ordering = ['name_product']

    # def get_absolute_url(self):
    #     """Returns the URL to access a detail record for this book."""
    #     return reverse('book-detail', args=[str(self.id)])


class Feedback(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, help_text='Unique ID for feedback')
    id_author = models.ForeignKey(User, on_delete=models.CASCADE)
    id_barcode = models.ForeignKey('Barcodes', on_delete=models.CASCADE)
    text = models.CharField(max_length=1200, help_text='text of feedback', null=True)
    time_creation = models.DateTimeField(blank=True)
    R_5 = 5
    R_4 = 4
    R_3 = 3
    R_2 = 2
    R_1 = 1
    RATES = (
        (R_1, 1),
        (R_2, 2),
        (R_3, 3),
        (R_4, 4),
        (R_5, 5),
    )

    rating = models.IntegerField(
        choices=RATES,
        blank=False,
        help_text='Product rate',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id_author.username} - {self.id_barcode}'


class Photo(models.Model):
    id = models.AutoField(primary_key=True, help_text='Unique ID for image')
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.image