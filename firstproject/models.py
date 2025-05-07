from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Модель категорий игр"""
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

class Publisher(models.Model):
    """Модель издателей игр"""
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
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Designer(models.Model):
    """Модель дизайнеров игр"""
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
        verbose_name = "Дизайнер"
        verbose_name_plural = "Дизайнеры"
        ordering = ['last_name', 'first_name']
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name', 'birth_date'],
                name='unique_designer'
            )
        ]
        
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Game(models.Model):
    """Основная модель настольных игр"""
    title = models.CharField(
        max_length=200, 
        unique=True,
        verbose_name="Название игры"
    )
    description = models.TextField(
        verbose_name="Описание игры"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='games',
        verbose_name="Категория"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='games',
        verbose_name="Издатель"
    )
    designers = models.ManyToManyField(
        Designer,
        related_name='games',
        verbose_name="Дизайнеры"
    )
    min_players = models.PositiveSmallIntegerField(
        verbose_name="Минимальное количество игроков",
        validators=[MinValueValidator(1)]
    )
    max_players = models.PositiveSmallIntegerField(
        verbose_name="Максимальное количество игроков",
        validators=[MinValueValidator(1)]
    )
    play_time = models.PositiveSmallIntegerField(
        verbose_name="Среднее время игры (минуты)",
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
    image = models.ImageField(
        upload_to='games/covers/',
        verbose_name="Обложка игры",
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
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['title']
        indexes = [
            models.Index(fields=['title'], name='game_title_idx'),
            models.Index(fields=['price'], name='game_price_idx'),
            models.Index(fields=['release_date'], name='game_release_date_idx'),
        ]
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})

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
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

class Stock(models.Model):
    """Модель складских остатков"""
    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
        related_name='stock',
        verbose_name="Игра"
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
        return f"{self.game.title}: {self.quantity} шт."