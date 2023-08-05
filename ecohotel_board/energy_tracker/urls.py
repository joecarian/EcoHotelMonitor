"""
URL patterns for the energy report application.

This module defines the URL patterns for the energy report application, mapping the URLs to the corresponding views.

URL Patterns:
    - '' (empty string): Maps to the EnergyReportListView view, displaying the home page.
    - 'create/': Maps to the CreateReportView view, allowing users to create new energy reports.
    - 'dashboard/': Maps to the DashboardView view, providing a dashboard for energy report statistics.
"""

from django.urls import path
from .views import EnergyReportListView, CreateReportView, DashboardView

urlpatterns = [
    path('', EnergyReportListView.as_view(), name='home'),
    path('create/', CreateReportView.as_view(), name='create_report'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view')
]
