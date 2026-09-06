import json
from datetime import datetime

def standardize_aws_data(response, environment='prod'):
    """
    Converts AWS Cost Explorer response into a list of unified records.
    """
    records = []
    
    if not response or 'ResultsByTime' not in response:
        print("⚠️ AWS response missing 'ResultsByTime'")
        return records

    for period in response['ResultsByTime']:
        date_str = period['TimePeriod']['Start']
        cost = float(period['Total']['UnblendedCost']['Amount'])
        
        record = {
            'provider': 'AWS',
            'resource_id': 'aws-account-total',
            'resource_type': 'Compute',
            'environment': environment,
            'cost': cost,
            'cpu_util_avg': None,
            'memory_util_avg': None,
            'usage_date': date_str,
            'raw_data': json.dumps(period)
        }
        records.append(record)
    
    return records


def standardize_azure_data(response, environment='prod'):
    """
    Converts Azure Cost Management response into a list of unified records.
    """
    records = []
    
    if hasattr(response, 'as_dict'):
        response = response.as_dict()
    
    if not response or 'rows' not in response:
        print("⚠️ Azure response missing 'rows'")
        return records

    columns = [col['name'].lower() for col in response.get('columns', [])]
    
    for row in response.get('rows', []):
        row_data = dict(zip(columns, row))
        
        cost = float(row_data.get('cost', 0))
        date_str = row_data.get('date', '')[:10]
        
        if not date_str:
            continue
            
        record = {
            'provider': 'Azure',
            'resource_id': row_data.get('resourceid', 'azure-account-total'),
            'resource_type': row_data.get('servicefamily', 'Compute'),
            'environment': environment,
            'cost': cost,
            'cpu_util_avg': None,
            'memory_util_avg': None,
            'usage_date': date_str,
            'raw_data': json.dumps(row_data)
        }
        records.append(record)
    
    return records


def standardize_gcp_data(response, environment='prod'):
    """
    Converts GCP BigQuery response into a list of unified records.
    """
    records = []
    
    if not response:
        print("⚠️ GCP response is empty")
        return records

    for row in response:
        record = {
            'provider': 'GCP',
            'resource_id': getattr(row, 'resource_id', 'gcp-unknown'),
            'resource_type': getattr(row, 'service_name', 'Compute'),
            'environment': environment,
            'cost': float(getattr(row, 'cost', 0)),
            'cpu_util_avg': None,
            'memory_util_avg': None,
            'usage_date': getattr(row, 'usage_date', datetime.now()).strftime('%Y-%m-%d'),
            'raw_data': str(row)
        }
        records.append(record)
    
    return records

