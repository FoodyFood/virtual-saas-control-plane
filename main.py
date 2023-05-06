# Inport our control plane services
from services.TenantManagement import TenantManagement
from services.UserManagement import UserManagement
from services.OnboardingManagement import OnboardingManagement


# Instanciate all the pieces of the control plane
tenant_management: TenantManagement = TenantManagement()
user_management: UserManagement = UserManagement()


# Inform the onboarding management service about the other parts of the control plane
onboarding_management: OnboardingManagement = OnboardingManagement(tenant_management, user_management)


def billing_management():
    pass


def provisioning():
    pass


def main():

    # Onboard some tenants/users
    onboarding_management.register("user_email_1@customer_1.com", "customer_1", "billing address")
    print("")
    onboarding_management.register("user_email_2@customer_1.com", "customer_1", "billing address")
    print("")
    onboarding_management.register("user_email_1@customer_2.com", "customer_2", "billing address")
    print("")
    onboarding_management.register("user_email_1@customer_1.com", "customer_1", "billing address") # Including creating a duplicate
    print("")

    # Delete a tenant
    print("\nList of users for customer_1: ", user_management.get_users_for_tenant(tenant_management.get_tenant_id("customer_1")))
    print("Tenant ID for customer_1: ",tenant_management.get_tenant_id("customer_1"))
    onboarding_management.unregister("user_email@customer.com", "customer_1", "billing address")
    print("Tenant ID for customer_1: ", tenant_management.get_tenant_id("customer_1"))
    print("List of users for customer_1 after deleting tenant: ", user_management.get_users_for_tenant(tenant_management.get_tenant_id("customer_1")), "\n")


if __name__ == '__main__':
    main()
