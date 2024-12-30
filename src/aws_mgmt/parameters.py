import boto3
from botocore.exceptions import ClientError

# Make sure you get the region right. You ran into a ParameterNotFound exception when you used an incorrect region
def get_parameter(parameter_name: str, region_name: str = "us-east-2"):
    """
    :param parameter_name: Name of parameter in AWS System Manager's parameter store
    :param region_name: Region of the parameter
    :return: parameter value if it exists or returns None
    """
    ssm_client = boto3.client('ssm', region_name)
    try:
        response = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except ClientError as e:
        print(f"Error retrieving parameter {parameter_name}: {e}")
        return None

print(get_parameter("DISCORD_APP_ID", "us-east-2"))