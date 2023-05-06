import os
import uuid
import signal


# Fake databases
tenants: list[dict[str, str]] = []
users: list[dict[str, str]] = []


class TenantManagement():
    def create_tenant(self, customer_shortname: str = None) -> str:
        if(customer_shortname == None):
            return None

        # Check if we already have a tenant id for this customer
        for tenant in tenants:
            if tenant[0] == customer_shortname:
                # IF we do, return it instead of generating a new one
                return tenant[1]

        # If we get to here there was no tenant id found for the customer so we generate one
        tenant_id = uuid.uuid4()

        # We add our new tenant id to the tenant database
        tenants.append([customer_shortname, tenant_id])

        # And we return the newly generated tenant id
        return(tenant_id)

    def get_tenant_id(self, customer_shortname: str = None) -> str:
        if(customer_shortname == None):
            return None

        # Check if we have a tenant id for this customer
        for tenant in tenants:
            if tenant[0] == customer_shortname:
                # IF we do, return it instead of generating a new one
                return tenant[1]

        # If none was found, return none
        return None

    def delete_tenant(self, tenant_id: str = None) -> bool:
        if(tenant_id == None):
            return None

        # Check if we already have a tenant id for this customer
        for tenant in tenants:
            if tenant[1] == tenant_id:
                # IF we do, return it instead of generating a new one
                tenants.remove([tenant[0], tenant[1]])
                return(True)
        return(False)
    


def user_management():
    pass


def billing_management():
    pass


def provisioning():
    pass


class Registration():
    _tenant_management: TenantManagement

    def __init__(self, tenant_management: TenantManagement):
        self._tenant_management = tenant_management


    def register(self, email: str = None, customer_shortname: str = None, billing_Address: str = None) -> bool:
        tenant_id: str = self._tenant_management.create_tenant(customer_shortname)
        print(f"Tenant ID for {customer_shortname} is: {tenant_id}")
    

    def unregister(self, email: str = None, customer_shortname: str = None, billing_Address: str = None) -> bool:
        tenant_id: str = self._tenant_management.get_tenant_id(customer_shortname)
        print(f"Deleting tenant: {customer_shortname}")
        self._tenant_management.delete_tenant(tenant_id)


# Graceful exit if user pressed CTRL + C
def signal_handler(sig, frame):
    """Ignore this"""
    print('')  # Empty on purpose, it formats better in terminal
    sys.exit(0)


def main():
    # Ignore these
    os.system('clear')
    signal.signal(signal.SIGINT, signal_handler)


    # Instanciate all the pieces of the control plane
    tenant_management: TenantManagement = TenantManagement()


    # Inform the registration microservice about the other parts of the control plane
    registration: Registration = Registration(tenant_management)


    # Register some tenants
    registration.register("user_email@customer.com", "customer_1", "billing address")
    registration.register("user_email@customer.com", "customer_2", "billing address")
    registration.register("user_email@customer.com", "customer_1", "billing address") # Including creating a duplicate

    # Delete a tenant
    print("\nTenant ID for customer_1: ", tenant_management.get_tenant_id("customer_1"))
    registration.unregister("user_email@customer.com", "customer_1", "billing address")
    print("Tenant ID for customer_1: ", tenant_management.get_tenant_id("customer_1"), "\n")


if __name__ == '__main__':
    main()
