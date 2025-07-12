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
