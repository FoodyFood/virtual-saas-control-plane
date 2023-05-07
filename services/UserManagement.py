from services.IdentityManagement import IdentityManagement


class UserManagement():
    _identity_management: IdentityManagement

    def __init__(self):
        self._identity_management = IdentityManagement()

    def create_user(self, tenant_id: str = None, email: str = None) -> bool:
        if (tenant_id == None or email == None):
            return None

        # Tell the identity management service to add the user
        self._identity_management.add_user(tenant_id=tenant_id, email=email)
        return True

    def get_tenant_users(self, tenant_id: str = None):
        if (tenant_id == None):
            return None

        list_of_users: list[dict[str,str]] = self._identity_management.get_list_of_users()

        list_of_tenant_users: list[dict[str, str]] = []

        for user in list_of_users:
            if (user[0] == tenant_id):
                list_of_tenant_users.append(user)

        return (list_of_tenant_users)

    def delete_user(self, user: dict[str, str]) -> bool:
        if (user == None):
            return None

        self._identity_management.delete_user(user)
        return True
