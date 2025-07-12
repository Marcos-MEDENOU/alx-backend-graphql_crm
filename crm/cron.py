"""
Cron jobs for the CRM application.
"""
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Log a heartbeat message and verify GraphQL endpoint.
    """
    # Format the timestamp
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"
    
    # Log to file
    with open('/tmp/crm_heartbeat_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_message)
    
    # Optional: Verify GraphQL endpoint
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            use_json=True,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
        query {
            hello
        }
        """)
        result = client.execute(query)
        if result.get('hello'):
            with open('/tmp/crm_heartbeat_log.txt', 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} GraphQL endpoint is responsive\n")
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} GraphQL check failed: {str(e)}\n")

def update_low_stock():
    """
    Update low stock products by executing a GraphQL mutation.
    Logs the updates to a file.
    """
    from datetime import datetime
    from gql import gql, Client
    from gql.transport.requests import RequestsHTTPTransport
    import json
    
    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        use_json=True,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Define the mutation
    mutation = gql("""
    mutation UpdateLowStock($amount: Int!) {
        updateLowStockProducts(restockAmount: $amount) {
            success
            message
            updatedProducts {
                id
                name
                stock
            }
        }
    }
    """)
    
    try:
        # Execute the mutation
        result = client.execute(mutation, variable_values={"amount": 10})
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare log message
        log_message = f"\n=== Low Stock Update - {timestamp} ===\n"
        
        if result.get('updateLowStockProducts', {}).get('success'):
            updated_products = result['updateLowStockProducts'].get('updatedProducts', [])
            log_message += f"Success: {result['updateLowStockProducts']['message']}\n"
            
            if updated_products:
                log_message += "Updated products:\n"
                for product in updated_products:
                    log_message += f"- {product['name']}: Stock updated to {product['stock']}\n"
            else:
                log_message += "No products were updated.\n"
        else:
            log_message += "Error: Failed to update low stock products\n"
        
        # Write to log file
        with open('/tmp/low_stock_updates_log.txt', 'a', encoding='utf-8') as f:
            f.write(log_message)
            
        return log_message
        
    except Exception as e:
        error_message = f"Error in update_low_stock: {str(e)}"
        with open('/tmp/low_stock_updates_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n=== Error - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n{error_message}\n")
        return error_message
