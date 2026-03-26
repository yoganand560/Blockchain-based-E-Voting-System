# ⛓ BlockVote — Blockchain-Based E-Voting System
![image alt](Google_Play_store-AnalysisImage_tzv9qztzv9qztzv9.png)
> A secure, transparent, and tamper-proof electronic voting system built on blockchain technology.

---

## 📌 Overview

**BlockVote** is a Python-based e-voting application that treats every vote as a blockchain transaction. Once a vote is recorded, it becomes a permanent, immutable block in the chain — making any tampering immediately detectable through cryptographic hash verification.

This project demonstrates real-world application of:
- Blockchain data structures
- SHA-256 cryptographic hashing
- Proof of Work (PoW) consensus mechanism
- Voter anonymization & authentication
- Chain integrity verification

---

## 🔐 Core Security Principles

| Principle | How It's Implemented |
|-----------|----------------------|
| **Authentication** | Only pre-registered Voter IDs can cast votes |
| **Anonymity** | Voter ID is hashed with SHA-256 before storage — identity is never recorded |
| **Accuracy** | Hash-based tracking ensures each voter can only vote once |
| **Verifiability** | Any node can independently re-verify the entire chain |
| **Immutability** | Altering any vote breaks the hash chain — instantly exposing tampering |

---

## 🗂 Project Structure

```
blockvote/
│
├── blockchain_evoting.py     # Core blockchain backend (Python)
├── blockchain_evoting.html   # Interactive frontend demo (browser)
└── README.md                 # This file
```

---

## ⚙️ How It Works

### 1. Voter Authentication
```
Enter Voter ID → Validated against registered voter list → Rejected if already voted
```

### 2. Vote Anonymization
```python
voter_hash = hashlib.sha256(voter_id.encode()).hexdigest()[:16]
# Original ID is never stored — only the hash
```

### 3. Block Mining (Proof of Work)
```python
while not self.hash.startswith("00"):   # difficulty = 2
    self.nonce += 1
    self.hash = self.calculate_hash()
```

### 4. Chain Linking
Each block stores the hash of the previous block:
```
[Genesis Block] → [Block #1: Vote] → [Block #2: Vote] → ...
  hash: 00a3f...   prev: 00a3f...     prev: 00b7c...
                   hash: 00b7c...     hash: 00e1d...
```

### 5. Tamper Detection
```python
def verify_chain(self):
    for i in range(1, len(self.chain)):
        if current.hash != current.calculate_hash():   # Hash mismatch
            return False
        if current.previous_hash != previous.hash:     # Broken link
            return False
    return True
```

---

## 🚀 Getting Started

### Requirements
- Python 3.7+
- No external libraries required (uses built-in `hashlib`, `json`, `uuid`)

### Run the Python Backend

```bash
python3 blockchain_evoting.py
```

**Sample output:**
```
=== Blockchain E-Voting System Demo ===

Vote by VOTER001 for Party Alpha: ✓
  Block #1 | Hash: 006ec111... | Nonce: 241
Vote by VOTER002 for Party Beta: ✓
  Block #2 | Hash: 00b2ca48... | Nonce: 30

Duplicate vote attempt: Voter has already voted

=== Election Results ===
  Party Alpha: 3 votes
  Party Beta:  1 vote
  Party Gamma: 1 vote
  Party Delta: 0 votes

Chain integrity: Chain is valid
```

### Run the Interactive Frontend

Simply open `blockchain_evoting.html` in any modern browser — no server needed.

---

## 🧱 Class Architecture

### `Vote`
Represents a single anonymized vote.
```python
Vote(voter_id, party)
  .voter_id   → SHA-256 hash of original ID (anonymized)
  .party      → Selected candidate party
  .timestamp  → Unix timestamp
  .vote_id    → Unique vote identifier (UUID)
```

### `Block`
A block in the chain containing vote transactions.
```python
Block(index, votes, previous_hash)
  .calculate_hash()   → SHA-256 of block contents
  .mine_block(diff)   → Proof of Work — finds valid nonce
```

### `Blockchain`
Manages the full chain, voters, and election logic.
```python
Blockchain(difficulty=2)
  .cast_vote(voter_id, party)   → Authenticate, record, mine
  .get_results()                → Tally all votes
  .verify_chain()               → Validate cryptographic integrity
  .get_chain_data()             → Export full chain as JSON
```

---

## 🗳 Registered Voters (Demo)

The demo system includes 10 pre-registered voters:

```
VOTER001  VOTER002  VOTER003  VOTER004  VOTER005
VOTER006  VOTER007  VOTER008  VOTER009  VOTER010
```

You can register additional voters programmatically:
```python
blockchain.register_voter("VOTER011")
```

---

## 🔬 Tamper Detection Demo

Try modifying a vote after it's been cast:

```python
bc = Blockchain()
bc.cast_vote("VOTER001", "Party Alpha")

# Tamper with the vote
bc.chain[1].votes[0].party = "Party Beta"

# Verify — this will now FAIL
valid, msg = bc.verify_chain()
print(msg)  # → "Block 1 hash mismatch"
```

---

## 📊 Candidate Parties

| Party | Symbol |
|-------|--------|
| Party Alpha | α |
| Party Beta | β |
| Party Gamma | γ |
| Party Delta | δ |

---

## 🛡 Security Considerations

- **Proof of Work** (difficulty=2) makes rewriting history computationally expensive
- **Voter anonymization** ensures votes cannot be linked back to identities
- **One-vote enforcement** is cryptographically guaranteed via hashed voter tracking
- **Chain verification** can be run by any independent observer at any time

> ⚠️ This is an educational project. A production voting system would also require a distributed network of nodes, digital signatures, a secure registration authority, and formal security audits.

---

## 💡 Concepts Demonstrated

- ✅ Python OOP (classes, encapsulation)
- ✅ Cryptographic hashing (SHA-256)
- ✅ Blockchain data structure (linked blocks)
- ✅ Proof of Work consensus
- ✅ Data anonymization
- ✅ Chain integrity verification
- ✅ Frontend-backend system design

---

## 👨‍💻 Built With

- **Python 3** — Core blockchain logic
- **hashlib** — SHA-256 cryptography
- **HTML/CSS/JavaScript** — Interactive demo frontend
- **Web Crypto API** — Browser-side hashing

---

*BlockVote — Making every vote count, permanently.*
