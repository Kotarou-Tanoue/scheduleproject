from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),

    path('contact/', views.ContactView.as_view(), name = 'contact'),

    path('post_schedule/', views.CreateScheduleView.as_view(), name = 'post_schedule'),

    path('delete_done/', views.DeleteSuccessView.as_view(), name = 'delete_done'),

    path('schedule_detail/<int:pk>/', views.ScheduleDetailView.as_view(), name = 'schedule_detail'),

    path('schedule/<int:category>/', views.CategoryView.as_view(), name = 'schedule_cat'),

    path('schedule/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name = 'schedule_delete'),

    path('schedule/<int:pk>/update/', views.ScheduleUpdateView.as_view() , name = 'schedule_update'),

    path('schedule/calendar_index/', views.calendar_view, name = 'calendar_index'),

    path('schedule/calendar/', views.get_events, name = 'get_events'),
]