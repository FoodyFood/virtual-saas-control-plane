# Fake list of provisioned infra
provisioned_infra: list[dict[str, str]] = []


class ProvisioningManagement():
    def provision(self, tenant_id: str = None, tier: str = None):
        for infra in provisioned_infra:
            if infra == [tenant_id, tier]:
                return True

        provisioned_infra.append([tenant_id, tier])

    def get_infra_for_tenant(self, tenant_id: str = None) -> dict[str,str]:
        if tenant_id == None:
            return False
        for infra in provisioned_infra:
            if infra[0] == tenant_id:
                return infra
        return False

    def unprovision(self, tenant_id: str = None):
        for infra in provisioned_infra:
            if infra[0] == tenant_id:
                provisioned_infra.remove(infra)
                return True
