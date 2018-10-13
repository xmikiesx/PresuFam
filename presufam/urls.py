from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'presufam'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('log-out/', login_required(views.LogOutView.as_view()), name='log-out'),
    path('del-out/', login_required(views.MyUserDeleteView.as_view), name='del-account'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('upd-user/<int:pk>', login_required(views.UpdateView.as_view), name='upd-user'),
    path('add-income/', login_required(views.IncomeCreate.as_view()), name='add-income'),
    path('upd-income/<int:pk>', login_required(views.IncomeUpdate.as_view()), name='upd-income'),
    path('del-income/<int:pk>', login_required(views.IncomeDelete.as_view()), name='del-income'),
    path('income/', login_required(views.IncomeIndexView.as_view()), name='income'),
    path('add-expense/', login_required(views.ExpenseCreate.as_view()), name='add-expense'),
    path('upd-expense/<int:pk>', login_required(views.ExpenseUpdate.as_view()), name='upd-expense'),
    path('del-expense/<int:pk>', login_required(views.ExpenseDelete.as_view()), name='del-expense'),
    path('expense/', login_required(views.ExpenseIndexView.as_view()), name='expense'),
    path('budget/', views.BudgetView.as_view(), name='budget'),
]