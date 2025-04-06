from django.shortcuts import render
from django.db import connection

from django.shortcuts import render
from django.db import connection

def backup_view(request):
    tables = []
    
    # Fetch all table names (compatible with MySQL)
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")  # MySQL query to list tables
        tables = [row[0] for row in cursor.fetchall()]

    return render(request, 'backup_view.html', {'tables': tables})



from django.http import HttpResponse
import json

def get_table_data(request):
    table_name = request.GET.get('table', '')
    
    if not table_name:
        return HttpResponse("Invalid table name", status=400)

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")  # Fetch first 10 records
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    html = "<table border='1' cellpadding='5'><tr>"
    html += "".join(f"<th>{col}</th>" for col in columns)
    html += "</tr>"

    for row in rows:
        html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
    
    html += "</table>"

    return HttpResponse(html)
