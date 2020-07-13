
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('З','Зима'),
    ('Д','Демисезон'),
    ('У','Уставные'),
    ('К','Классика'),
    ('Л','Лето'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ShoeSize(models.Model):
    rusSize = models.FloatField(("Размер RU"), max_length=10, help_text="Выберите все размеры для модели")

    def __str__(self):
        return self.rusSize


class Product(models.Model):

    title           = models.CharField(("Название модели"),max_length=100)
    price           = models.FloatField(("Цена"))
    discount_price  = models.FloatField(("Скидка"),blank=True, null=True)
    category        = models.CharField(("Категории"),choices=CATEGORY_CHOICES, max_length=2)
    slug            = models.SlugField()
    description     = models.TextField(("Описание модели"),)
    image1          = models.ImageField(("Картинка1"), blank=True, null=True)
    image2          = models.ImageField(("Картинка2"), blank=True, null=True)
    image3          = models.ImageField(("Картинка3"), blank=True, null=True)
    image4          = models.ImageField(("Картинка4"), blank=True, null=True)
    weight          = models.IntegerField(("Вес"),)

    dimensions      = models.CharField(("Размеры"), max_length=256)
    topMaterial     = models.CharField(("Материал верха"), max_length=256)
    liningMaterial  = models.CharField(("Название модели"), max_length=256)
    soleMaterial    = models.CharField(("Название модели"), max_length=256)
    color           = models.CharField(("Цвет"), max_length=256)
    clasp           = models.CharField(("Застежка"), max_length=256)
    insole          = models.CharField(("Стелька"), max_length=256)
    outsoleMount    = models.CharField(("Крепление подошвы"), max_length=256)
    height          = models.CharField(("Высота"), max_length=256)
    rusSize         = models.ManyToManyField(ShoeSize, related_name="sizes", blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "slug": self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
    

class OrderItem(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered     = models.BooleanField(("Упорядочено"),default=False)
    item        = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField(("Количество"),default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price 
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Address(models.Model):
    user                =  models.ForeignKey(settings.AUTH_USER_MODEL,
                                             on_delete=models.CASCADE)
    city                = models.CharField(("Город"), max_length=100)
    street_address      = models.CharField(("Улица"), max_length=100)  
    building            = models.CharField(("Дом"), max_length=100)
    zipcode             = models.CharField(("Количество"), max_length=100)
    default             = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
    

class Order(models.Model):
    user                = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)
    items               = models.ManyToManyField(OrderItem)
    shipping_address    = models.ManyToManyField(Address)
    shipped             = models.BooleanField(default=False)

    created_at          = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        
        return total

"""


    + + + + + + +    + + + +       + + + +      + + + + + +   + + + + + +  ++  + + + + + +   +            + +
    +           +   +       +     +        +    +             +            ++  +             +            +    +
    +           +  +         +   +          +   +             +                +             +            +     +
    +              +            +            +  +             +            ++  +             +            +      +
    + + + + + + +  +            +            +  + + + +       + + + +      ++  + + + + + +   +            +      +
                +  +            +            +  +             +            ++  +             +            +      +
                +  +         +   +           +  +             +            ++  +             +            +     +
                +   +       +     +         +   +             +            ++  +             +            +    +
    + + + + + + +    + + + +       + + + + +    +             +            ++  + + + + + +   + + + + + +  + + 


"""