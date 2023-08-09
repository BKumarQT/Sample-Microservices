import uuid


class TransactionManager:
    async def generate_lattice_transaaction_id(self):
        """
        Description: Function to generate lattice transaction id
        Parameters: po_data
        Returns: Latttice transaction id
        """
        return str(uuid.uuid4())

transaction_manager = TransactionManager()