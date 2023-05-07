# Inport our control plane services
from services.TenantManagement import TenantManagement
from services.UserManagement import UserManagement
from services.BillingManagement import BillingManagement
from services.ProvisioningManagement import ProvisioningManagement


class OnboardingManagement():
    _tenant_management: TenantManagement
    _user_management: UserManagement
    _billing_management: BillingManagement
    _provisioning_management: ProvisioningManagement

    def __init__(self, tenant_management: TenantManagement, user_management: UserManagement, billing_management: BillingManagement, provisioning_management: ProvisioningManagement):
        self._tenant_management = tenant_management
        self._user_management = user_management
        self._billing_management = billing_management
        self._provisioning_management = provisioning_management

    def register(self, email: str = None, customer_name: str = None, billing_address: str = None, tier: str = None) -> bool:
        # Create a Tenant ID
        print("Calling tenant management service to create or fetch tenant id")
        tenant_id: str = self._tenant_management.create_tenant(customer_name=customer_name, tier=tier)
        print(f"Tenant ID for {customer_name} is: {tenant_id}")

        # Create the user
        print(f"Calling user management service to create user: {email} for customer: {customer_name}")
        self._user_management.create_user(email=email, tenant_id=tenant_id)

        # Create the billing entity
        print("Calling the billing management service to create the billing entity")
        self._billing_management.create_billing_entity(tenant_id=tenant_id, billing_address=billing_address)

        # Provision infra
        print("Calling the provisioning management service to create the infra for the tenant")
        self._provisioning_management.provision(tenant_id=tenant_id, tier=tier)

    def unregister(self, email: str = None, customer_name: str = None, tenant_id: str = None) -> bool:
        '''
        Must pass 1 of either customer_name or tenant_id
        Will clean up all users first, then delete the tenant.
        '''
        
        if(tenant_id == None):
            tenant_id: str = self._tenant_management.get_tenant_id(customer_name)

        # Unprovision infra
        print("Calling the provisioning management service to delete the infra for the tenant")
        self._provisioning_management.unprovision(tenant_id=tenant_id)

        # Delete the billing entity
        print("Calling the billing management service to delete the billing entity")
        self._billing_management.delete_billing_entity(tenant_id=tenant_id)

        print(f"Calling user management service to delete users for tenant: {tenant_id}")
        for user in self._user_management.get_tenant_users(tenant_id=tenant_id):
            self._user_management.delete_user(user=user)

        print(f"CAlling tenant management service to delete tenant: {customer_name}")
        self._tenant_management.delete_tenant(tenant_id)
