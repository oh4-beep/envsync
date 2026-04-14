import firebase_admin
from firebase_admin import credentials, firestore

class BaseVault:
    def push(self, project_name, encrypted_data):
        raise NotImplementedError
    
    def pull(self, project_name):
        raise NotImplementedError

class FirestoreVault(BaseVault):
    def __init__(self, service_account_path):
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def push(self, project_name, encrypted_data):
        self.db.collection("envsync").document(project_name).set({
            "env": encrypted_data,
            "updated_at": firestore.SERVER_TIMESTAMP
        })

    def pull(self, project_name):
        doc = self.db.collection("envsync").document(project_name).get()
        if not doc.exists:
            raise Exception(f"No env found for project: {project_name}")
        return doc.to_dict()["env"]