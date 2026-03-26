import hashlib
import json
import time
import uuid
from datetime import datetime


class Vote:
    def __init__(self, voter_id, party):
        self.voter_id = hashlib.sha256(voter_id.encode()).hexdigest()[:16]  # Anonymize
        self.party = party
        self.timestamp = time.time()
        self.vote_id = str(uuid.uuid4())[:8]

    def to_dict(self):
        return {
            "voter_hash": self.voter_id,
            "party": self.party,
            "timestamp": self.timestamp,
            "vote_id": self.vote_id
        }


class Block:
    def __init__(self, index, votes, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.votes = votes
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": [v.to_dict() for v in self.votes],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty=2):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.nonce

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "votes": [v.to_dict() for v in self.votes],
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.pending_votes = []
        self.used_voters = set()
        self.difficulty = difficulty
        self.parties = ["Party Alpha", "Party Beta", "Party Gamma", "Party Delta"]
        self.registered_voters = set([
            "VOTER001", "VOTER002", "VOTER003", "VOTER004", "VOTER005",
            "VOTER006", "VOTER007", "VOTER008", "VOTER009", "VOTER010"
        ])
        # Create genesis block
        genesis = Block(0, [], "0" * 64)
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)

    def register_voter(self, voter_id):
        self.registered_voters.add(voter_id)
        return True

    def cast_vote(self, voter_id, party):
        # Authentication
        if voter_id not in self.registered_voters:
            return {"success": False, "error": "Voter not registered"}

        # Check one-vote rule
        voter_hash = hashlib.sha256(voter_id.encode()).hexdigest()[:16]
        if voter_hash in self.used_voters:
            return {"success": False, "error": "Voter has already voted"}

        # Validate party
        if party not in self.parties:
            return {"success": False, "error": "Invalid party selection"}

        # Record vote (anonymized)
        vote = Vote(voter_id, party)
        self.pending_votes.append(vote)
        self.used_voters.add(voter_hash)

        # Add block when we have 3 votes (or immediately for demo)
        block = self.add_block([vote])

        return {
            "success": True,
            "vote_id": vote.vote_id,
            "block_index": block.index,
            "block_hash": block.hash[:20] + "...",
            "nonce": block.nonce
        }

    def add_block(self, votes):
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), votes, previous_hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def get_results(self):
        tally = {p: 0 for p in self.parties}
        for block in self.chain[1:]:  # Skip genesis
            for vote in block.votes:
                if vote.party in tally:
                    tally[vote.party] += 1
        return tally

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False, f"Block {i} hash mismatch"
            if current.previous_hash != previous.hash:
                return False, f"Block {i} broken link"
        return True, "Chain is valid"

    def get_chain_data(self):
        return [block.to_dict() for block in self.chain]

    def get_stats(self):
        total_votes = sum(1 for block in self.chain[1:] for _ in block.votes)
        return {
            "total_blocks": len(self.chain),
            "total_votes": total_votes,
            "voters_remaining": len(self.registered_voters) - len(self.used_voters),
            "chain_valid": self.verify_chain()[0]
        }


# Demo run
if __name__ == "__main__":
    bc = Blockchain(difficulty=2)
    print("=== Blockchain E-Voting System Demo ===\n")

    # Cast some votes
    test_votes = [
        ("VOTER001", "Party Alpha"),
        ("VOTER002", "Party Beta"),
        ("VOTER003", "Party Alpha"),
        ("VOTER004", "Party Gamma"),
        ("VOTER005", "Party Alpha"),
    ]

    for voter_id, party in test_votes:
        result = bc.cast_vote(voter_id, party)
        print(f"Vote by {voter_id} for {party}: {'✓' if result['success'] else '✗'}")
        if result["success"]:
            print(f"  Block #{result['block_index']} | Hash: {result['block_hash']} | Nonce: {result['nonce']}")

    # Duplicate vote attempt
    dup = bc.cast_vote("VOTER001", "Party Beta")
    print(f"\nDuplicate vote attempt: {dup['error']}")

    print(f"\n=== Election Results ===")
    for party, count in bc.get_results().items():
        print(f"  {party}: {count} votes")

    valid, msg = bc.verify_chain()
    print(f"\nChain integrity: {msg}")
    print(f"Total blocks: {len(bc.chain)} | Total votes: {sum(bc.get_results().values())}")
