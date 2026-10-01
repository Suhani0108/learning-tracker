from django.urls import path

from . import views

# app_name lets templates refer to these URLs as "topics:list", "topics:detail"
app_name = "topics"

urlpatterns = [
    # /  -> list of the user's topics
    path("", views.topic_list, name="list"),
    # /topics/new/  -> form to add a topic
    path("topics/new/", views.topic_create, name="create"),
    # /topics/3/  -> topic with id 3 (<int:...> only matches whole numbers)
    path("topics/<int:topic_id>/", views.topic_detail, name="detail"),
    path("topics/<int:topic_id>/edit/", views.topic_edit, name="edit"),
    path("topics/<int:topic_id>/delete/", views.topic_delete, name="delete"),
    # Resources (links) belonging to a topic
    path("topics/<int:topic_id>/resources/add/", views.resource_add, name="resource_add"),
    path("resources/<int:resource_id>/delete/", views.resource_delete, name="resource_delete"),
]
