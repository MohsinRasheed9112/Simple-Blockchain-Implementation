import hashlib
import datetime as date

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature 

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature,
        }

    def sign(self, signature):
        self.signature = signature

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_header = str(self.index) + str(self.timestamp) + str(self.previous_hash) + str(self.nonce)
        block_transactions = "".join([str(tx.to_dict()) for tx in self.transactions])
        hash_string = block_header + block_transactions
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: ", self.hash)

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        # Validate pending transactions; simplistic check
        valid_transactions = [tx for tx in self.pending_transactions if self.validate_transaction(tx)]

        if not valid_transactions:
            print("No valid transactions to mine.")
            return

        block = Block(len(self.chain), date.datetime.now(), valid_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)

        print("Block successfully mined!")
        self.chain.append(block)

        # Reset pending transactions and send mining reward
        self.pending_transactions = [Transaction(None, mining_reward_address, self.mining_reward)]

    def create_transaction(self, transaction):
        # In real-world scenarios, you should validate and sign transactions here
        self.pending_transactions.append(transaction)

    def validate_transaction(self, transaction):
        # Placeholder for more complex validation; checks basic conditions
        if transaction.amount <= 0:
            return False
        if not transaction.sender or not transaction.recipient:
            return False
        # Additional validation logic (e.g., signature verification) would go here
        return True

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Example usage
blockchain = Blockchain()
blockchain.create_transaction(Transaction("Abdullah", "Mohsin", 100))
blockchain.create_transaction(Transaction("Mohsin", "Hassan", 50))

print("Starting the miner...")
blockchain.mine_pending_transactions("Miner's Address")

blockchain.create_transaction(Transaction("Mohsin", "Ali", 30))
blockchain.create_transaction(Transaction("Ali", "Mohsin", 20))

print("\nStarting the miner again...")
blockchain.mine_pending_transactions("Miner's Address 2")
print("\n")

# Print the contents of the blockchain
for block in blockchain.chain:
    print("Block #" + str(block.index))
    print("Timestamp:", block.timestamp)
    print("Transactions:")
    for tx in block.transactions:
        print(f"    {tx.sender} -> {tx.recipient}: {tx.amount} units")
    print("Nonce:", block.nonce)
    print("Current Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("\n")
