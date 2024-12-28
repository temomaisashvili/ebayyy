from django.utils import timezone
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Category Name")

    def __str__(self):
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="username")
    first_name = models.CharField(max_length=100, verbose_name="name", default="")
    email = models.EmailField("email", unique=False)
    is_active = models.BooleanField("active", default=False)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(blank=False, null=False)
    seller = models.ForeignKey(Customer, related_name="products", on_delete=models.CASCADE)
    price = models.IntegerField(null=False, blank=False)
    discount_percentage = models.IntegerField(default=0)
    stock = models.PositiveIntegerField()
    listing_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart of {self.user.name}"

    def add_item(self, product, quantity=1):
        if product.stock < quantity:
            raise ValidationError("not in stock.")
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        product.stock -= quantity
        product.save()
        return cart_item

    def get_total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())
class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        blank=True,
        null=False,
        related_name="items",
        on_delete=models.CASCADE,
    )

    cart = models.ForeignKey(
        Cart,
        null=False,
        blank=False,
        related_name="cart_items",
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} - {self.cart}"

    def total_price(self):
        # return self.quantity * self.product.price
        pass

