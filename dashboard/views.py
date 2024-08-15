from django.contrib.auth.decorators import login_required
from django.db import connection
from core.models import SearchLog
from django.db.models import Count
from django.shortcuts import render

@login_required
def admin_dashboard(request):

    search_logs = SearchLog.objects.all().order_by('-search_timestamp')
    recent_20 = search_logs[:20]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_database_size(current_database());")
        db_size = cursor.fetchone()[0]

    top_results = (search_logs
                   .values('top_result')
                   .annotate(result_count=Count('top_result'))
                   .order_by('-result_count')[:10])
    
    most_common_top_result = top_results.first()['top_result'] if top_results else 'N/A'

    class_names = [result['top_result'] for result in top_results]
    class_counts = [result['result_count'] for result in top_results]


    db_size_gb = db_size / (1024 * 1024 * 1024)
    db_size_gb = round(db_size_gb, 4)
    num_searches = search_logs.count()
    

    context = {
        'search_logs': recent_20,
        'db_size': db_size_gb,
        'num_searches': num_searches,
        'most_common_top_result': most_common_top_result,
        'class_names': class_names,
        'class_counts': class_counts
    }

    
    return render(request, 'dashboard/base.html', context)