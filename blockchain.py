import hashlib
import time 
import json

class Block :
    #Constructor for a block
    def __init__(self,index , transactions,prev_hash,diff=2):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.diff = diff
        self.hash = self.compute_hash()
    # Hash For the blokc will be computed here
    def compute_hash(self):
        block = json.dumps({
            "index" : self.index,
            'timestamp' : self.timestamp,
            'transactions' : self.transactions,
            'prev_hash' : self.prev_hash,
            'nonce' : self.nonce
        },sort_keys=True).encode()
        return hashlib.sha256(block).hexdigest()
    
    def mine_block(self):
        while not self.hash.startswith("0"*self.diff):
            self.nonce +=1
            self.hash = self.compute_hash()

class BlockChain:
    #COnstructor which will create a blockchain
    def __init__(self,diff=2):
        self.chain = []
        self.diff = diff
        self.create_block()

        #New Blocks will be created in the chain
    def create_block(self):
        block = Block(0,"Genesis Block","0" , self.diff)
        block.mine_block()
        self.chain.append(block)
    #To append the blocks
    def add_block(self,transaction):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain),transaction,prev_block.hash,self.diff)
        new_block.mine_block()
        self.chain.append(new_block)
    #Check the validity if the block is tampered or not
    def is_valid(self):
        for i in range(1,len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]

            if current.hash!=current.compute_hash():
                return False
            if current.prev_hash != prev.hash:
                return False
        return True
    #Printing the blockchain
    def print_chain(self):
        for block in self.chain:
            print (json.dumps({
                'index' : block.index,
                'timestamp' : block.timestamp,
                'transactions' : block.transactions,
                'prev_hash' : block.prev_hash,
                'hash' : block.hash
            },indent=4))


#Block Chain Demonstration
blockchain = BlockChain(diff=3)
blockchain.add_block(['John Pays Doe 4 BTC'])
blockchain.add_block(['Jane Pays Smith 2 BTC'])
blockchain.add_block(['Bob pays Marley 10 BTC'])

print("Before Tampering")
blockchain.print_chain()
print("Is Chain Valid?? : ",blockchain.is_valid())

blockchain.chain[1].transactions = ['Bob pays John 50 BTC']

print("\n Block Chain After Tampering: ")
blockchain.print_chain()
print("Is Chain Valid?? : ", blockchain.is_valid())
