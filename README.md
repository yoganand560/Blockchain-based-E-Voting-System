# ⛓ BlockVote — Blockchain-Based E-Voting System

![image alt](https://github.com/yoganand560/Blockchain-based-E-Voting-System/blob/e66cfc133d84fade200c660f9af83b7fcda780d7/Blockchain-based-E-Voting%20system.png)

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

## ✨ What's New — Election Setup Page

A **⚙️ Setup** button has been added to the header of the frontend. It opens a setup modal that lets you fully configure the election **before it starts** — without changing anything about the core voting system.

### What you can configure:

#### 👤 Number of Voters (1–100)
- Use the **+/−** buttons to increase or decrease the voter count one at a time
- Or use the **quick preset buttons**: 5 · 10 · 25 · 50 · 100
- Voters are automatically registered as `VOTER001`, `VOTER002`, … up to your chosen count

#### 🏛 Parties (1–10)
- **Add** new parties (up to a maximum of 10)
- **Remove** any party using the 🗑 button
- For each party you can customise:
  - 🎨 **Colour** — click the colour dot to open a colour picker
  - ✏️ **Name** — edit the party name inline
  - 🖼 **Logo / Symbol** — click the logo button to pick an emoji from the grid, or type any character

#### ✓ Apply & Start Election
- Clicking **Apply & Start Election** commits all changes, resets the blockchain, and rebuilds the voting UI instantly with your new configuration

> ⚠️ Applying setup resets the election and clears all previously cast votes.

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

To configure the election before voting, click the **⚙️ Setup** button in the top-right corner of the page.

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

The default demo includes 10 pre-registered voters:

```
VOTER001  VOTER002  VOTER003  VOTER004  VOTER005
VOTER006  VOTER007  VOTER008  VOTER009  VOTER010
```

You can change the voter count (1–100) at any time via the **⚙️ Setup** page, or register additional voters programmatically in the Python backend:
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

## 📊 Candidate Parties (Default)

| Party | Symbol | Colour |
|-------|--------|--------|
| Party Alpha | α | 🟢 `#00d4aa` |
| Party Beta  | β | 🔵 `#3b82f6` |
| Party Gamma | γ | 🟡 `#f59e0b` |
| Party Delta | δ | 🟣 `#a78bfa` |

> Parties, their names, symbols, and colours can all be changed from the **⚙️ Setup** page before the election begins.

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
- ✅ Dynamic election configuration (Setup page)

---

## 👨‍💻 Built With

- **Python 3** — Core blockchain logic
- **hashlib** — SHA-256 cryptography
- **HTML/CSS/JavaScript** — Interactive demo frontend
- **Web Crypto API** — Browser-side hashing

---

*BlockVote — Making every vote count, permanently.*
