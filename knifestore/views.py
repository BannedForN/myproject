from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from basket.forms import BasketAddProductForm


@login_required
def user_orders(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('-order_date')
    return render(request, 'orders/user_orders.html', {'orders': orders})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Или куда хочешь перенаправить
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправляем после входа
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Или куда хочешь после выхода

# Create your views here.
def home(request):
    return render(request, 'home.html')

class KnifeStoreView(ListView):
    model = Knife
    template_name = 'store/knife_store.html'
    context_object_name = 'knifes'

class KnifeListView(ListView):
    model = Knife
    template_name = 'knife_list.html'
    context_object_name = 'knifes'
    paginate_by = 10
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Создаем диапазон от 1 до 10 для выбора количества ед.
        context['range'] = range(1, 11)
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметр количества ед. из запроса GET
        players = self.request.GET.get('players')

        # Фильтруем по количеству ед., если параметр указан
        if players:
            queryset = queryset.filter(min_players__lte=players, max_players__gte=players)
        
        return queryset

class KnifeDetailView(DetailView):
    model = Knife
    template_name = 'knife_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_basket'] = BasketAddProductForm()
        return context
        
    
class KnifeCreateView(CreateView):
    model = Knife
    fields = '__all__'
    template_name = 'knife_form.html'
    success_url = reverse_lazy('knife_list')

class KnifeUpdateView(UpdateView):
    model = Knife
    fields = '__all__'
    template_name = 'knife_form.html'
    success_url = reverse_lazy('knife_list')

class KnifeDeleteView(DeleteView):
    model = Knife
    template_name = 'knife_confirm_delete.html'
    success_url = reverse_lazy('knife_list')
    
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.count()
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['knifes'] = self.object.knifes.all()  # Используем related_name из модели Knife
        return context

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

class BrandListView(ListView):
    model = Brand
    template_name = 'brands/brand_list.html'
    context_object_name = 'publishers'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_publishers'] = Brand.objects.count()
        return context

class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brands/brand_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['knifes'] = Knife.objects.filter(publisher=self.object)
        return context

class BrandCreateView(CreateView):
    model = Brand
    fields = ['name', 'country', 'website', 'founded']
    template_name = 'brands/brand_form.html'
    success_url = reverse_lazy('brand_list')

class BrandUpdateView(UpdateView):
    model = Brand
    fields = ['name', 'country', 'website', 'founded']
    template_name = 'brands/brand_form.html'
    success_url = reverse_lazy('brand_list')

class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'brands/brand_confirm_delete.html'
    success_url = reverse_lazy('brand_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['knifes'] = self.object.knifes.all()
        return context
    
class SeriesListView(ListView):
    model = Series
    template_name = 'series/series_list.html'
    paginate_by = 15
    context_object_name = 'series_list'

class SeriesDetailView(DetailView):
    model = Series
    template_name = 'series/series_detail.html'

class SeriesCreateView(CreateView):
    model = Series
    fields = ['first_name', 'last_name', 'birth_date', 'country']
    template_name = 'series/series_form.html'
    success_url = reverse_lazy('series_list')

class SeriesUpdateView(UpdateView):
    model = Series
    fields = ['first_name', 'last_name', 'birth_date', 'country']
    template_name = 'series/series_form.html'
    success_url = reverse_lazy('series_list')

class SeriesDeleteView(DeleteView):
    model = Series
    template_name = 'series/series_confirm_delete.html'
    success_url = reverse_lazy('series_list')

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 15
    ordering = ['-registration_date']

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'

class CustomerCreateView(CreateView):
    model = Customer
    fields = ['user', 'phone', 'address', 'birth_date']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['phone', 'address', 'birth_date']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    ordering = ['-order_date']

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class OrderCreateView(CreateView):
    model = Order
    fields = ['customer', 'status', 'shipping_address']
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset'] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            self.object.update_total()  # Обновляем общую сумму
            return super().form_valid(form)
        
        return self.render_to_response(self.get_context_data(form=form))

class OrderUpdateView(UpdateView):
    model = Order
    fields = ['customer', 'status', 'shipping_address']
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            self.object.update_total()
            return super().form_valid(form)
        
        return self.render_to_response(self.get_context_data(form=form))

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'order_items/orderitem_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return OrderItem.objects.all().select_related('order', 'knife')

class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = 'order_items/orderitem_detail.html'

class OrderItemCreateView(CreateView):
    model = OrderItem
    form_class = OrderItemFormSet
    template_name = 'orderitem_form.html'
    success_url = reverse_lazy('orderitem_list')

class OrderItemUpdateView(UpdateView):
    model = OrderItem
    form_class = OrderItemFormSet
    template_name = 'orderitem_form.html'
    success_url = reverse_lazy('orderitem_list')

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'order_items/orderitem_confirm_delete.html'
    success_url = reverse_lazy('orderitem_list')

class StockListView(ListView):
    model = Stock
    template_name = 'stock/stock_list.html'
    context_object_name = 'stock_list'

class StockCreateView(CreateView):
    model = Stock
    fields = ['knife', 'quantity']
    template_name = 'stock/stock_form.html'
    success_url = reverse_lazy('stock_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['knife'].queryset = Knife.objects.exclude(stock__isnull=False)
        return form

class StockUpdateView(UpdateView):
    model = Stock
    fields = ['quantity']
    template_name = 'stock/stock_form.html'
    success_url = reverse_lazy('stock_list')

class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'stock/stock_confirm_delete.html'
    success_url = reverse_lazy('stock_list')