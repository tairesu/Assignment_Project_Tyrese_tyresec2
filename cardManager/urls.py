from django.urls import path, include
from cardManager import views 

urlpatterns = [
	path('card/<str:card_token>/', views.card_detail, name='card_view'),
	path('card/<str:card_token>/activate/', views.CardDetail.as_view(), name='card_activate_view'),
	path('card/<str:card_token>/fbv-update/', views.card_update, name='card_update_view'),
	path('card/<str:card_token>/class-update/', views.CardUpdate.as_view(), name='card_class_update_view'),
	path('profile/<str:profile_slug>/', views.ProfileDetail.as_view(), name='profile_view'),
	path('profile/<str:profile_slug>/update', views.ProfileUpdate.as_view(), name='profile_update_view'),
	path('dashboard/', views.UserDashboard.as_view(), name='dashboard_view'),
	path('stats/', views.Stats.as_view(), name='stats_view'),
	path('stats/fetch_plotly_data', views.config_plotly),
	path('api/daily_usage/', views.daily_usage, name='api_daily_usage_view'),
	path('api/daily_usage/bar_graph.png', views.daily_usage_png, name='daily_usage_graph_png_view'),
]