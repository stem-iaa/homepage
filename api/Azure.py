from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
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

    network_client = NetworkManagementClient(
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

    @staticmethod
    def get_vm_ip(name):
        instance = Azure.compute_client.virtual_machines.get(
            Azure.RESOURCE_GROUP, name
        )

        try:
            network_interface_name = instance.network_profile.network_interfaces[0].id.split("/")[-1]
            public_ip_name = Azure.network_client.network_interfaces.get(
                Azure.RESOURCE_GROUP, network_interface_name
            ).ip_configurations[0].public_ip_address.id.split("/")[-1]
            public_ip_obj = Azure.network_client.public_ip_addresses.get(Azure.RESOURCE_GROUP, public_ip_name)
            ip_address = public_ip_obj.ip_address
            return ip_address
        except:
            return None


if __name__ == '__main__':
    print(Azure.get_vm_ip("studentone"))
