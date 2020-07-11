from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order/<str:category>", views.order_route, name="order"),
    path("login", views.login_route, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_route, name="logout"),
    path("cart", views.cart, name="cart"),
    path("submit", views.submitOrder, name="submit"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("add/<str:category>/<str:name>/<str:price>", views.add, name="add")
]
