from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    """
    Generate a weekly CRM report with total customers, orders, and revenue.
    Logs the report to /tmp/crm_report_log.txt
    """
    try:
        # Setup GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            use_json=True,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Define the GraphQL query
        query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """)

        # Execute the query
        result = client.execute(query)
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare the report
        report = (
            f"{timestamp} - Report: "
            f"{result.get('totalCustomers', 0)} customers, "
            f"{result.get('totalOrders', 0)} orders, "
            f"${result.get('totalRevenue', 0):.2f} revenue\n"
        )
        
        # Write to log file
        with open('/tmp/crm_report_log.txt', 'a', encoding='utf-8') as f:
            f.write(report)
            
        return report
        
    except Exception as e:
        error_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error generating CRM report: {str(e)}\n"
        with open('/tmp/crm_report_log.txt', 'a', encoding='utf-8') as f:
            f.write(error_message)
        return error_message
