import os
import uuid
import signal


# Fake databases
tenants: list[dict[str, str]] = [] # customer_shortname, tenant_id
users:  list[dict[str, str, str]] = [] # email, customer_shortname, tenant_id


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
    


class UserManagement():
    def create_user(self, email: str = None, customer_shortname: str = None, tenant_id: str = None) -> bool:
        if(email == None or customer_shortname == None or tenant_id == None):
            return None

        # Check if the user already exists in the database
        for user in users:
            if(user[0] == email and user[1] == customer_shortname and user[2] == tenant_id):
                return True # User already exists

        # Add the user to the users database
        users.append([email, customer_shortname, tenant_id])
        return True

    def get_users_for_tenant(self, tenant_id: str = None):
        if(tenant_id == None):
            return None

        list_of_users_for_tenant: list[dict[str, str, str]] = []

        for user in users:
            if(user[2] == tenant_id):
                list_of_users_for_tenant.append(user)

        return(list_of_users_for_tenant)

    def delete_user(self, user) -> bool:
        if(user == None):
            return None
        
        users.remove(user)
        return True
        



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
