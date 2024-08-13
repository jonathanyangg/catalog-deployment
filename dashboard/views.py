from django.contrib.auth.decorators import login_required
from core.models import SearchLog
from django.shortcuts import render

@login_required
def admin_dashboard(request):

    search_logs = SearchLog.objects.all().order_by('-search_timestamp')

    context = {
        'search_logs': search_logs
    }

    
    return render(request, 'dashboard/base.html', context)