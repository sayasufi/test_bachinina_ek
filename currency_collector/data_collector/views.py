from datetime import datetime

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import CurrencyRate, Currency


def show_rates(request):
    date_query = request.GET.get('date', None)
    if date_query:
        try:
            date = datetime.strptime(date_query, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        rates = CurrencyRate.objects.filter(date=date)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if rates.exists():
                data = [{'currency': rate.currency.char_code, 'value': rate.value} for rate in rates]
            else:
                data = []
            return JsonResponse(data, safe=False)

        return render(request, 'rates.html', {'rates': rates, 'date': date_query})
    return render(request, 'rates.html')


def fetch_currency(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        if url:
            response = requests.get(url)
            data = response.json()

            date = datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%S%z').date()
            for code, info in data['Valute'].items():
                currency, created = Currency.objects.get_or_create(
                    char_code=info['CharCode'],
                    defaults={'name': info['Name']}
                )

                CurrencyRate.objects.update_or_create(
                    currency=currency,
                    date=date,
                    defaults={'value': info['Value']}
                )
            return JsonResponse({'status': 'success', 'message': 'Data successfully updated'})
        return JsonResponse({'status': 'error', 'message': 'URL is required'}, status=400)
    elif request.method == 'GET':
        # Возврат страницы с формой для отправки URL
        return render(request, 'fetch_data.html')
    return HttpResponse('Method not allowed', status=405)
