from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from app import config
from app import db


class Azure:
    credentials = ServicePrincipalCredentials(
        client_id=config["azure"]["client_id"],
        secret=config["azure"]["secret"],
        tenant=config["azure"]["tenant"]
    )

    compute_client = ComputeManagementClient(
        credentials,
        config["azure"]["subscription_id"]
    )

    RESOURCE_GROUP = "stem-iaa2"

    @staticmethod
    def start_vm(name):
        return Azure.compute_client.virtual_machines.start(Azure.RESOURCE_GROUP, name)

    @staticmethod
    def get_vm_status(name):
        statuses = [status.code for status in Azure.compute_client.virtual_machines.get(
            Azure.RESOURCE_GROUP, name, expand="instanceView"
        ).instance_view.statuses]

        status_messages = {}
        for status in statuses:
            split = status.split("/")
            status_messages[split[0]] = split[1]

        return status_messages.get("PowerState")


if __name__ == '__main__':
    print(Azure.get_vm_status("random"))
