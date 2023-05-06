# Inport our control plane services
from services.TenantManagement import TenantManagement
from services.UserManagement import UserManagement


class OnboardingManagement():
    _tenant_management: TenantManagement
    _user_management: UserManagement

    def __init__(self, tenant_management: TenantManagement, user_management: UserManagement):
        self._tenant_management = tenant_management
        self._user_management = user_management

    def register(self, email: str = None, customer_shortname: str = None, billing_Address: str = None) -> bool:
        # Create a Tenant ID
        print("Calling tenant management service to create or fetch tenant id")
        tenant_id: str = self._tenant_management.create_tenant(
            customer_shortname=customer_shortname)
        print(f"Tenant ID for {customer_shortname} is: {tenant_id}")

        # Create the user
        print(
            f"Calling user management service to create user: {email} for customer: {customer_shortname}")
        self._user_management.create_user(
            email=email, customer_shortname=customer_shortname, tenant_id=tenant_id)

    def unregister(self, email: str = None, customer_shortname: str = None, billing_Address: str = None) -> bool:
        tenant_id: str = self._tenant_management.get_tenant_id(
            customer_shortname)

        print(
            f"Calling user management service to delete users for tenant: {tenant_id}")
        for user in self._user_management.get_users_for_tenant(tenant_id=tenant_id):
            self._user_management.delete_user(user=user)

        print(
            f"CAlling tenant management service to delete tenant: {customer_shortname}")
        self._tenant_management.delete_tenant(tenant_id)
