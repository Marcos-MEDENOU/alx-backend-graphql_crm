#!/bin/bash

# Customer Cleanup Script
# Deletes customers with no orders since a year ago
# Logs the number of deleted customers with timestamp

# Get the current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Define the Django project path (adjust this path according to your project structure)
PROJECT_PATH="/path/to/your/alx-backend-graphql_crm"

# Navigate to the project directory
cd "$PROJECT_PATH"

# Execute Django management command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
# Assuming you have a related field 'orders' in Customer model
inactive_customers = Customer.objects.filter(
    orders__isnull=True
).union(
    Customer.objects.exclude(
        orders__created_at__gte=one_year_ago
    )
).distinct()

# Count and delete inactive customers
count = inactive_customers.count()
if count > 0:
    inactive_customers.delete()
    print(count)
else:
    print(0)
" 2>/dev/null)

# Log the result with timestamp
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt

# Exit with success status
exit 0