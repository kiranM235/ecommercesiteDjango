from django.urls import path
from django.utils import html
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('categories', views.categories, name='categories'),
    path('product_list', views.product_list, name='product_list'),
    path('contact', views.contact, name="contact"),
    path('blog', views.blog, name="blog"),
    path('single_blog', views.single_blog, name='single_blog'),
    path('accounts/login/', auth_views.LoginView.as_view
    (template_name='login.html', 
    authentication_form = LoginForm ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path('elements', views.elements, name='elements'),
    path('about', views.about, name='about'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('address/', views.address, name="address"),
    path('checkout/', views.checkout, name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    path('orders/', views.orders, name="orders"),
    path('mobile/', views.mobile, name="mobile"),
    path('mobile/<slug:data>', views.mobile, name="mobiledata"),
    path('fridge/', views.fridge, name="fridge"),
    path('fridge/<slug:data>', views.fridge, name="fridgedata"),
    path('washingmachine/', views.washingmachine, name="washingmachine"),
    path('washingmachine/<slug:data>', views.washingmachine, name="washingmachinedata"),
    path('television/', views.television, name="television"),
    path('television/<slug:data>', views.television, name="televisiondata"),
    path('treadmill/', views.treadmill, name="treadmill"),
    path('treadmill/<slug:data>', views.treadmill, name="treadmilldata"),
    path('dumbbell/', views.dumbbell, name="dumbbell"),
    path('dumbbell/<slug:data>', views.dumbbell, name="dumbbelldata"),
    path('electronics/', views.electronics, name="electronics"),
    path('fashion/', views.fashion, name="fashion"),
    path('homeappliances/', views.homeappliances, name="homeappliances"),
    path('fitness/', views.fitness, name="fitness"),
    #path('fashion/<slug:data>', views.fashion, name="fashiondata"),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', 
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.
    as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('laptop/', views.laptop, name="laptop"),
    path('laptop/<slug:data>', views.laptop, name="laptopdata"),
    path('menzsummertopwear/', views.menzsummertopwear, name="menzsummertopwear"),
    path('menzsummertopwear/<slug:data>', views.menzsummertopwear, name="menzsummertopweardata"),
    path('menzsummerbottomwear/', views.menzsummerbottomwear, name="menzsummerbottomwear"),
    path('menzsummerbottomwear/<slug:data>', views.menzsummerbottomwear, name="menzsummerbottomweardata"),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('buy_now', views.buy_now, name="buy_now"),
    path('password-reset/', auth_views.PasswordResetView.as_view
    (template_name='password_reset.html', 
    form_class=MyPasswordResetForm), name="password_reset"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view
    (template_name='password_reset_done.html'), name="password_reset_done"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view
    (template_name='password_reset_complete.html'), name="password_reset_complete"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
    (template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('signup/', views.CustomerRegistrationView.as_view(), name="signup"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
