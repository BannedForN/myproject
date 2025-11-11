from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Модель категорий нож"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Название категории",
        help_text="Максимальная длина 100 символов"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        help_text="Необязательное поле"
    )
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Brand(models.Model):
    """Модель Бренд нож"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Название издательства"
    )
    country = models.CharField(
        max_length=50, 
        verbose_name="Страна"
    )
    website = models.URLField(
        verbose_name="Веб-сайт",
        blank=True
    )
    founded = models.PositiveSmallIntegerField(
        verbose_name="Год основания",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Series(models.Model):
    """Модель Серия нож"""
    first_name = models.CharField(
        max_length=50, 
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50, 
        verbose_name="Фамилия"
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=50, 
        verbose_name="Страна",
        default='Россия'
    )
    
    class Meta:
        verbose_name = "Серия"
        verbose_name_plural = "Серии"
        ordering = ['last_name', 'first_name']
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name', 'birth_date'],
                name='unique_designer'
            )
        ]
        
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Knife(models.Model):
    """Основная модель кухонных ножей"""
    title = models.CharField(
        max_length=200, 
        unique=True,
        verbose_name="Название Ножи"
    )
    description = models.TextField(
        verbose_name="Описание Ножи"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='knifes',
        verbose_name="Категория"
    )
    publisher = models.ForeignKey(Brand,
        on_delete=models.SET_NULL,
        null=True,
        related_name='knifes',
        verbose_name="Бренд"
    )
    designers = models.ManyToManyField(Series,
        related_name='knifes',
        verbose_name="Серия"
    )
    min_players = models.PositiveSmallIntegerField(
        verbose_name="Минимальная партия",
        validators=[MinValueValidator(1)]
    )
    max_players = models.PositiveSmallIntegerField(
        verbose_name="Максимальная партия",
        validators=[MinValueValidator(1)]
    )
    play_time = models.PositiveSmallIntegerField(
        verbose_name="Среднее время Ножи (минуты)",
        validators=[MinValueValidator(10)]
    )
    age_rating = models.PositiveSmallIntegerField(
        verbose_name="Рекомендуемый возраст",
        validators=[MinValueValidator(3), MaxValueValidator(18)]
    )
    release_date = models.DateField(
        verbose_name="Дата выпуска"
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Цена (руб)",
        validators=[MinValueValidator(0)]
    )

    # --- Knife-specific fields ---
    steel = models.CharField(
        max_length=100,
        verbose_name="Сталь",
        help_text="Например, VG-10, AUS-8, X50CrMoV15"
    )
    blade_length_mm = models.PositiveIntegerField(
        verbose_name="Длина лезвия (мм)",
        help_text="Например, 180"
    )
    PURPOSE_CHOICES = [
        ("CHEF", "Шефский"),
        ("SANTOKU", "Сантоку"),
        ("UTILITY", "Универсальный"),
        ("PARING", "Овощной/Нож для чистки"),
        ("BREAD", "Хлебный"),
        ("BONING", "Филе/Разделочный"),
        ("CLEAVER", "Тяпка"),
    ]
    purpose = models.CharField(
        max_length=16,
        choices=PURPOSE_CHOICES,
        verbose_name="Назначение"
    )
    edge_angle_deg = models.PositiveSmallIntegerField(
        verbose_name="Угол заточки (°)",
        help_text="Обычно 12–20° на сторону",
        validators=[MinValueValidator(8), MaxValueValidator(40)]
    )
    handle_material = models.CharField(
        max_length=100,
        verbose_name="Материал рукояти",
        help_text="Например, микарта, дерево, пластик"
    )
    manufacturer_country = models.CharField(
        max_length=100,
        verbose_name="Страна-производитель",
        blank=True
    )

    image = models.ImageField(
        upload_to='knives/covers/',
        verbose_name="Фото ножа",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )
    
    class Meta:
        verbose_name = "Нож"
        verbose_name_plural = "Ножи"
        ordering = ['title']
        indexes = [
            models.Index(fields=['title'], name='knife_title_idx'),
            models.Index(fields=['price'], name='knife_price_idx'),
            models.Index(fields=['release_date'], name='knife_release_date_idx'),
        ]
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('knife_detail', kwargs={'pk': self.pk})

class Customer(models.Model):
    """Модель покупателей"""
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name="Пользовательская запись",
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True
    )
    address = models.TextField(
        verbose_name="Адрес доставки",
        blank=True
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True
    )
    registration_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    
    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        ordering = ['-registration_date']
        
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else "Анонимный покупатель"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)  # Это поле было пропущено
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_address = models.TextField()
    
    def update_total(self):
        self.total_amount = sum(
            item.quantity * item.price 
            for item in self.items.all()
        )
        self.save(update_fields=['total_amount'])
    
    def __str__(self):
        return f"Заказ #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    knife = models.ForeignKey(Knife, on_delete=models.PROTECT)  # было: knife = ...
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

class Stock(models.Model):
    """Модель складских остатков"""
    knife = models.OneToOneField(
        Knife,
        on_delete=models.CASCADE,
        related_name='stock',
        verbose_name="Ножи"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество на складе",
        default=0
    )
    last_restocked = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее пополнение"
    )
    
    class Meta:
        verbose_name = "Складской остаток"
        verbose_name_plural = "Складские остатки"
        ordering = ['-last_restocked']
        
    def __str__(self):
        return f"{self.knife.title}: {self.quantity} шт."