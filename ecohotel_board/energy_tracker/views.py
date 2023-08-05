"""This module contains view-based classes for handling HTTP requests.

List of classes:
- EnergyReportListView: View for the main page of the site.
- CreateReportView: View for the "Add Report" page.
- DashboardView: View for the "Dashboard" page.
"""
from typing import Any, Dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EcoHotel, Report
from .forms import ReportForm, ECOHOTELS_CHOICES
from django.db.models import Sum

class EnergyReportListView(LoginRequiredMixin,ListView):
    """Class that manages the homepage view.

        Attributes:
            model (Report): instance of the model Report.
            template_name (str): name of the template of homepage.
    """
    model = Report
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Gets the context data for the template.

        Returns:
            Dict[str, Any]: the context data for template.
        """
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.all().order_by('-date').distinct()

        return context


class CreateReportView(View):
    """Class that manages the form view for create report.
    """

    def get(self, request):
        """Handles the GET request.
            Args:
                request (HttpRequest): The HttpRequest object of the request.

            Returns:
                HttpResponse: the redirect to the homepage or JsonResponse with 400 status code.
        """
        form = ReportForm()
        return render(request, 'report_form.html', {'form': form})

    def post(self, request):
        """Handles the POST request.

        Args:
            request (HttpRequest): The HttpRequest object of the request.

        Returns:
            HttpResponse, JsonRepsone: redirect to homepage or JsonResponse with 400 status code. 
        """
        form = ReportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            energy_produced = form.cleaned_data['energy_produced']
            energy_consumed = form.cleaned_data['energy_consumed']
            name = form.cleaned_data.get('name', 'Pomelia')
            energy_produced = form.cleaned_data['energy_produced']
            energy_consumed = form.cleaned_data['energy_consumed']
            ecohotel = EcoHotel.objects.filter(
                name=ECOHOTELS_CHOICES[int(name)][1]).first()
            report = Report(
                ecohotel=ecohotel, energy_produced=energy_produced, energy_consumed=energy_consumed)
            report.write_on_chain()
            return redirect('/')
        else:
            response_data = {'result': 'failure', 'errors': form.errors}
            return JsonResponse(response_data, status=400)


class DashboardView(LoginRequiredMixin, View):
    """Class that manages the dashboard view for the admin.  
        Attributes:
            login_url (str): url of the login page.
    """
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        """Handles the GET request.
        Args:
            request (HttpRequest): The HttpRequest object of the request.
            args (tuple): Tuples of the positional arguments.
            kwargs (dict): Dictionary of named arguments.

        Returns:
            HttpResponse: the redirect to dashboard or access_denied page.
        """
        hotel_infos = []
        if request.user.is_staff:
            for hotel in EcoHotel.objects.all():
                total_consumed = sum(Report.objects.filter(ecohotel=hotel).values_list(
                    'energy_consumed', flat=True))
                total_produced = sum(Report.objects.filter(ecohotel=hotel).values_list(
                    'energy_produced', flat=True))
                total_prod_daily = Report.objects.filter(ecohotel=hotel).values('date').annotate(
                    total_energy=Sum('energy_produced')).order_by('-total_energy').first()
                total_consum_daily = Report.objects.filter(ecohotel=hotel).values('date').annotate(
                    total_energy=Sum('energy_consumed')).order_by('-total_energy').last()

                hotel_infos.append(
                    (hotel, {
                            'total_consumed': total_consumed,
                            'total_produced': total_produced,
                            'max_energy_prod_day': total_prod_daily.get('date', None),
                            'max_energy_prod': total_prod_daily.get('total_energy', None),
                            'max_energy_cons_day': total_consum_daily.get('date', None),
                            'max_energy_cons': total_consum_daily.get('total_energy', None)
                            }
                    )
                )

            context = {
                'hotels': hotel_infos
            }
                
            return render(request, 'dashboard.html', context)
        else:
            return render(request, 'access_denied.html')
