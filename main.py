# Inport our control plane services
from services.TenantManagement import TenantManagement
from services.UserManagement import UserManagement
from services.BillingManagement import BillingManagement
from services.OnboardingManagement import OnboardingManagement
from services.ProvisioningManagement import ProvisioningManagement


# Instanciate all the pieces of the control plane
tenant_management: TenantManagement = TenantManagement()
user_management: UserManagement = UserManagement()
billing_management: BillingManagement = BillingManagement()
provisioning_management: ProvisioningManagement = ProvisioningManagement()


# Inform the onboarding management service about the other services in the control plane
onboarding_management: OnboardingManagement = OnboardingManagement(tenant_management, user_management, billing_management, provisioning_management)


def main():

    # Onboard some tenants/users
    onboarding_management.register(email="user_email_1@customer_1.com", customer_name="customer_1", billing_address="customer 1 billing address", tier="standard")
    print("")
    onboarding_management.register(email="user_email_2@customer_1.com", customer_name="customer_1", billing_address="customer 1 billing address", tier="standard")
    print("")
    onboarding_management.register(email="user_email_1@customer_2.com", customer_name="customer_2", billing_address="customer 2 billing address", tier="premium")
    print("")
    onboarding_management.register(email="user_email_1@customer_1.com", customer_name="customer_1", billing_address="customer 1 billing address", tier="standard") # Including creating a duplicate
    print("")


    # Get tenant tier
    print("Tier for customer_1: ", tenant_management.get_tenant_tier(tenant_management.get_tenant_id("customer_1")))

    # Get custoemr_1 billing entity
    print("Billing entity for customer_1: ", billing_management.get_billing_entity_for_tenant(tenant_management.get_tenant_id("customer_1")))

    # Get customer_1 provisioned infra
    print("Provisioned infra for customer_1: ", provisioning_management.get_infra_for_tenant(tenant_management.get_tenant_id("customer_1")))


    # Delete customer_1 tenant
    print("\nList of users for customer_1: ", user_management.get_tenant_users((tenant_management.get_tenant_id("customer_1"))))
    print("Tenant ID for customer_1: ",tenant_management.get_tenant_id("customer_1"))
    onboarding_management.unregister(email="user_email@customer.com", customer_name="customer_1")
    print("Tenant ID for customer_1: ", tenant_management.get_tenant_id("customer_1"))
    print("List of users for customer_1 after deleting tenant: ", user_management.get_tenant_users(tenant_management.get_tenant_id("customer_1")), "\n")


    # Get tenant 2 tier
    print("Tier for customer_2: ", tenant_management.get_tenant_tier(tenant_management.get_tenant_id("customer_2")))

    # Get custoemr_2 billing entity
    print("Billing entity for customer_2: ", billing_management.get_billing_entity_for_tenant(tenant_management.get_tenant_id("customer_2")))

    # Get customer_2 provisioned infra
    print("Provisioned infra for customer_2: ", provisioning_management.get_infra_for_tenant(tenant_management.get_tenant_id("customer_2")))

    # Generate invoice line items for tenant
    print("GEnerate line items for invoice using billing and metrics service: ", billing_management.generate_invoice(tenant_management.get_tenant_id("customer21")))



if __name__ == '__main__':
    main()
