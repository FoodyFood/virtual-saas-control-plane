import uuid

# Fake database
tenants: list[dict[str, str]] = [] # customer_shortname, tenant_id


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
    
