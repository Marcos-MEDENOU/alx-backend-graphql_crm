#!/bin/bash

# Get the current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Execute Django management command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
customers_to_delete = Customer.objects.filter(
    orders__isnull=True
) | Customer.objects.exclude(
    orders__created_at__gte=one_year_ago
)

# Count and delete inactive customers
count = customers_to_delete.distinct().count()
if count > 0:
    customers_to_delete.distinct().delete()
    print(count)
else:
    print(0)
")

# Log the result with timestamp
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt