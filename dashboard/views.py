from django.contrib.auth.decorators import login_required
from django.db import connection
from core.models import SearchLog
from django.db.models import Count
from django.shortcuts import render

@login_required
def admin_dashboard(request):

    search_logs = SearchLog.objects.all().order_by('-search_timestamp')
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_database_size(current_database());")
        db_size = cursor.fetchone()[0]

    top_results = (search_logs
                   .values('top_result')
                   .annotate(result_count=Count('top_result'))
                   .order_by('-result_count')[:10])
    
    most_common_top_result = top_results.first()['top_result'] if top_results else 'N/A'

    top_10 = {result['top_result']: result['result_count'] for result in top_results}
    top_10_keys = top_10.keys()
    top_10_vals = top_10.values()

    

    db_size_gb = db_size / (1024 * 1024 * 1024)
    db_size_gb = round(db_size_gb, 4)
    num_searches = search_logs.count()
    

    context = {
        'search_logs': search_logs,
        'db_size': db_size_gb,
        'num_searches': num_searches,
        'most_common_top_result': most_common_top_result,
        'top_10_keys': top_10_keys,
        'top_10_vals': top_10_vals
    }

    
    return render(request, 'dashboard/base.html', context)