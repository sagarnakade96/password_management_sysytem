from django.urls import path, include
from .views import user_entries, set_pin, user_entry_detail

urlpatterns = [
    path("list/", user_entries, name="entry_list"),
    path("details/", user_entry_detail, name="entry_list"),
    path("set_pin/", set_pin, name="set_pin_for_user"),
]
