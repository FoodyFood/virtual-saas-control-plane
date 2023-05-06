import os
import uuid
import signal

from services.TenantManagement import TenantManagement
from services.UserManagement import UserManagement




def billing_management():
    pass


def provisioning():
    pass


class Registration():
    _tenant_management: TenantManagement
    _user_management: UserManagement


    def __init__(self, tenant_management: TenantManagement, user_management: UserManagement):
        self._tenant_management = tenant_management
        self._user_management = user_management


    def register(self, email: str = None, customer_shortname: str = None, billing_Address: str = None) -> bool:
        # Create a Tenant ID
        print("Calling tenant management service to create or fetch tenant id")
        tenant_id: str = self._tenant_management.create_tenant(customer_shortname=customer_shortname)
        print(f"Tenant ID for {customer_shortname} is: {tenant_id}")

        # Create the user
        print(f"Calling user management service to create user: {email} for customer: {customer_shortname}")
        self._user_management.create_user(email=email, customer_shortname=customer_shortname, tenant_id=tenant_id)
    

    def unregister(self, email: str = None, customer_shortname: str = None, billing_Address: str = None) -> bool:
        tenant_id: str = self._tenant_management.get_tenant_id(customer_shortname)
        
        print(f"Calling user management service to delete users for tenant: {tenant_id}")
        for user in self._user_management.get_users_for_tenant(tenant_id=tenant_id):
            self._user_management.delete_user(user=user)

        print(f"CAlling tenant management service to delete tenant: {customer_shortname}")
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
    user_management: UserManagement = UserManagement()


    # Inform the registration microservice about the other parts of the control plane
    registration: Registration = Registration(tenant_management, user_management)


    # Register some tenants
    registration.register("user_email_1@customer_1.com", "customer_1", "billing address")
    print("")
    registration.register("user_email_2@customer_1.com", "customer_1", "billing address")
    print("")
    registration.register("user_email_1@customer_2.com", "customer_2", "billing address")
    print("")
    registration.register("user_email_1@customer_1.com", "customer_1", "billing address") # Including creating a duplicate
    print("")

    # Delete a tenant
    print("\nList of users for customer_1: ", user_management.get_users_for_tenant(tenant_management.get_tenant_id("customer_1")))
    print("Tenant ID for customer_1: ", tenant_management.get_tenant_id("customer_1"))
    registration.unregister("user_email@customer.com", "customer_1", "billing address")
    print("Tenant ID for customer_1: ", tenant_management.get_tenant_id("customer_1"))
    print("List of users for customer_1 after deleting tenant: ", user_management.get_users_for_tenant(tenant_management.get_tenant_id("customer_1")), "\n")


if __name__ == '__main__':
    main()
