import uuid

# Fake database
tenants: list[dict[str, str, str]] = []  # customer_name, tenant_id, tier


class TenantManagement():
    def create_tenant(self, customer_name: str = None, tier: str = None) -> str:
        if (customer_name == None or tier == None):
            return None

        # Check if we already have a tenant id for this customer
        for tenant in tenants:
            if tenant[0] == customer_name:
                # If we do, return it instead of generating a new one
                return tenant[1]

        # If we get to here there was no tenant id found for the customer so we generate one
        tenant_id = str(uuid.uuid4())

        # We add our new tenant id to the tenant database
        tenants.append([customer_name, tenant_id, tier])

        # And we return the newly generated tenant id
        return (tenant_id)

    def get_tenant_id(self, customer_name: str = None) -> str:
        if (customer_name == None):
            return None

        # Check if we have a tenant id for this customer
        for tenant in tenants:
            if tenant[0] == customer_name:
                # IF we do, return it instead of generating a new one
                return tenant[1]

        # If none was found, return none
        return None

    def get_tenant_customer_name(self, tenant_id: str = None) -> str:
        if (tenant_id == None):
            return None

        # Check if we have a tenant id for this customer
        for tenant in tenants:
            if tenant[1] == tenant_id:
                # IF we do, return it instead of generating a new one
                return tenant[0]

        # If none was found, return none
        return None

    def get_tenant_tier(self, tenant_id: str = None, customer_name: str = None) -> str:
        '''
        Must pass 1 of either tenant_id or customer_name
        Returns tenant tier as string if tenant exists
        '''

        if (tenant_id == None):
            tenant_id = self.get_tenant_id(customer_name=customer_name)

        # Check if we already have a tenant id for this customer
        for tenant in tenants:
            if tenant[1] == tenant_id:
                return (tenant[2])

        # If none was found, return none
        return None

    def delete_tenant(self, tenant_id: str = None) -> bool:
        if (tenant_id == None):
            return None

        # Check if we already have a tenant id for this customer
        for tenant in tenants:
            if tenant[1] == tenant_id:
                # IF we do, return it instead of generating a new one
                tenants.remove(tenant)
                return (True)
        return (False)
