from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("create",views.create, name="create"),
    path("rand", views.rand, name="rand"),
    path("edit/<str:title>",views.edit, name="edit"),
    path("wiki/<str:title>", views.page, name="page")
    
]
