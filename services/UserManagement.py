# Fake databases
users:  list[dict[str, str]] = []  # tenant_id, email


class UserManagement():
    def create_user(self, tenant_id: str = None, email: str = None) -> bool:
        if (tenant_id == None or email == None):
            return None

        # Check if the user already exists in the database
        for user in users:
            if (user[0] == email and user[1] == tenant_id):
                return True  # User already exists

        # Add the user to the users database
        users.append([tenant_id, email])
        return True

    def get_tenant_users(self, tenant_id: str = None):
        if (tenant_id == None):
            return None

        list_of_tenant_users: list[dict[str, str]] = []

        for user in users:
            if (user[0] == tenant_id):
                list_of_tenant_users.append(user)

        return (list_of_tenant_users)

    def delete_user(self, user: dict[str, str]) -> bool:
        if (user == None):
            return None

        users.remove(user)
        return True
