from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views import generic

from django.urls import reverse, reverse_lazy
from .models import MyUser, Income, Category, Expense
from .forms import MyUserUpdateForm, MyUserForm, SignInForm, IncomeForm, IncomeUpdateForm, ExpenseForm, ExpenseUpdateForm, CategoryForm

from django.db.models import Func, Sum, Q


class IndexView(View):
    def get(self, request):
        return render(request, 'presufam/index.html')


class SignInView(View):
    form = SignInForm()

    def get(self, request):
        context = {'form': self.form}
        return render(request, 'presufam/sign-in.html', context)

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect('presufam:profile')
                else:
                    context = {'form': self.form, 'msg': 'Usuario no está activo!'}
            else:
                context = {'form': self.form, 'msg': 'Error: Email - Password Invalido'}

            return render(request, 'presufam/sign-in.html', context)


class LogOutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect('presufam:index')


class SignUpView(View):
    form_class = MyUserForm
    template_name = 'presufam/sign-up.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # cleaned (normalized) data
            email = form.clean_email()
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                request.session['id'] = user.id
                return redirect('presufam:profile')

        return render(request, self.template_name, {'form': form})


class UserUpdate(UpdateView):
    model = MyUser
    form_class = MyUserUpdateForm
    template_name = 'presufam/manage-user.html'

    def get_success_url(self):
        return reverse('presufam:profile')


class ProfileView(View):
    def get(self, request):
        return render(request, 'presufam/profile.html', {'user': MyUser.objects.get(pk=request.session['id'])})


class MyUserDeleteView(View):
    def get(self, request):
        db = DB()
        db.delete_account(request.session['id'])
        return redirect('presufam:log-out')


class IncomeCreate(View):
    def get_initial(self):
        return {'user': self.request.session['id']}

    form_class = IncomeForm
    template_name = 'presufam/manage-income.html'

    # display blank form
    def get(self, request):
        form = self.form_class(request.user, None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('presufam:income')

        return render(request, self.template_name, {'form': form})


class IncomeUpdate(UpdateView):
    model = Income
    form_class = IncomeUpdateForm
    template_name = 'presufam/manage-income.html'

    def get_success_url(self):
        return reverse('presufam:income')


class IncomeDelete(DeleteView):
    model = Income
    success_url = reverse_lazy('presufam:income')


class IncomeIndexView(generic.ListView):
    template_name = 'presufam/income.html'
    context_object_name = 'all_income'
    paginate_by = 6

    def get_queryset(self):
        qname = self.request.GET.get("nombre")
        qdate = self.request.GET.get("fecha")
        us_id = self.request.session['id']
        if qname and qdate:
            return Income.objects.filter(
                Q(name__icontains=qname),
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('nombre')
        elif qname:
            return Income.objects.filter(
                Q(name__icontains=qname),
                user_id=us_id,
            ).order_by('-fecha')

        elif qdate:
            return Income.objects.filter(
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('nombre')

        return Income.objects.filter(user_id=us_id).order_by('-fecha')

    def get_context_data(self, **kwargs):
        us_id = self.request.session['id']
        context = super(IncomeIndexView, self).get_context_data(**kwargs)
        context['tincome'] = Income.objects.filter(user_id=us_id).aggregate(Sum('monto'))
        return context


class BudgetView(View):
    def get(self, request):
        return render(request, 'presufam/budget.html')


class ExpenseCreate(View):
    def get_initial(self):
        return {'user': self.request.session['id']}

    form_class = ExpenseForm
    template_name = 'presufam/manage-expense.html'

    def get(self, request):
        form = self.form_class(request.user, None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('presufam:expense')

        return render(request, self.template_name, {'form': form})


# Create Object Income to Update in DataBase
class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseUpdateForm
    template_name = 'presufam/manage-expense.html'

    def get_success_url(self):
        return reverse('presufam:expense')


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('presufam:expense')


class ExpenseIndexView(generic.ListView):
    template_name = "presufam/expense.html"
    context_object_name = 'all_expense'
    paginate_by = 6

    def get_queryset(self):
        qname = self.request.GET.get("nombre")
        qdate = self.request.GET.get("fecha")
        us_id = self.request.session['id']
        if qname and qdate:
            return Expense.objects.filter(
                Q(name__icontains=qname),
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('name')
        elif qname:
            return Expense.objects.filter(
                Q(name__icontains=qname),
                user_id=us_id,
            ).order_by('-fecha')

        elif qdate:
            return Expense.objects.filter(
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('nombre')

        return Expense.objects.filter(user_id=us_id).order_by('-fecha')

    def get_context_data(self, **kwargs):
        us_id = self.request.session['id']
        context = super(ExpenseIndexView, self).get_context_data(**kwargs)
        context['texpense'] = Expense.objects.filter(user_id=us_id).aggregate(Sum('monto'))
        return context


class CategoryIndexView(generic.ListView):
    template_name = 'presufam/overview.html'
    context_object_name = 'all_categories'
    paginate_by = 2

    def get_queryset(self):
        return Category.objects.filter(user_id=self.request.session['id']).order_by('-nombre')

    def get_context_data(self, **kwargs):
        db = DB()
        total = float(db.savings_per_user(self.request.session['id']))

        context = super(CategoryIndexView, self).get_context_data(**kwargs)
        context['savings'] = total
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'presufam/detail.html'


class CategoryCreate(View):
    form_class = CategoryForm
    template_name = 'presufam/manage-category.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            cnt = Category.objects.filter(user_id=request.user.id, nombre=category.nombre).count()

            if cnt == 0:
                category.save()

            return redirect('presufam:index')

        return render(request, self.template_name, {'form': form})


class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'presufam/manage-category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('presufam:index')


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('presufam:index')