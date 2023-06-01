from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings

CONDITION_CHOICES = (
    ('New', 'Nowy'),
    ('Used', 'Używany'),
    ('Damaged', 'Uszkodzony'),
)

class Category(MPTTModel):
  name = models.CharField(max_length=255, unique=True)
  parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
  slug = models.SlugField(max_length=255, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  
  class MPTTMeta:
    order_insertion_by = ['name']

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    value = self.name
    if not self.slug:
      self.slug = slugify(value, allow_unicode=True)
    super().save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse('items-by-category', args=[str(self.slug)])


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField( null=True, blank=True, default='/DefaultLocker.jpg')
    image2 = models.ImageField( null=True, blank=True, default='/DefaultLocker.jpg')
    image3 = models.ImageField( null=True, blank=True, default='/DefaultLocker.jpg')
    image4 = models.ImageField( null=True, blank=True, default='/DefaultLocker.jpg')
    brand = models.CharField(max_length=200, null=True, blank=True)
    descripption = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2,null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2,null=True, blank=True)
    createdt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    location = models.CharField(max_length=200, null=True, blank=True)
    condition = models.CharField(max_length=14, choices=CONDITION_CHOICES, default='provide')
    phoneNumber = models.CharField(max_length=12, default='000000000')
    category = TreeForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(
      max_length=255,
      default=name,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      kwargs = {
        'slug': self.slug
      }
      return reverse('item-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
      if not self.slug:
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
      super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"