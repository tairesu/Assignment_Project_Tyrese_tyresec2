from django.urls import path, include
from cardManager import views 
# A11
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path('card/<str:card_token>/', views.card_detail, name='card_view'),
	path('card/<str:card_token>/activate/', views.CardActivate.as_view(), name='card_activate_view'),
	path('card/<str:card_token>/fbv-update/', views.card_update, name='card_update_view'),
	path('card/<str:card_token>/class-update/', views.CardUpdate.as_view(), name='card_class_update_view'),
	path('profile/create/', views.ProfileCreate.as_view(), name='profile_create_view'),
	path('profile/slug/<str:profile_slug>/', views.ProfileDetail.as_view(), name='profile_view'),
	path('profile/slug/<str:profile_slug>/update', views.ProfileUpdate.as_view(), name='profile_update_view'),
	path('dashboard/', views.UserDashboard.as_view(), name='dashboard_view'),
	path('stats/fetch_plotly_data', views.config_plotly),
	path('api/daily_usage/', views.daily_usage, name='api_daily_usage_view'),
	path('api/daily_usage/bar_graph.png', views.daily_usage_png, name='daily_usage_graph_png_view'),
	path('order/create/', views.order_create, name='order_card_view'),
	path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail_view'),
	# A11: CSV & JSON Exports
	path('reports/', views.Stats.as_view(), name='stats_view'),
	path('export/usage.csv', views.export_usage_csv, name='export_usage_csv_view'),
	path('export/usage.json', views.export_usage_json, name='export_usage_json_view'),
	# A11: Access Control & Authentication
	path('login/', views.CustomLoginView.as_view(), name='login_view'),
	path('logout/', LogoutView.as_view(), name='logout_view'),
	path('signup/', views.signup_view, name="signup_view"),
]