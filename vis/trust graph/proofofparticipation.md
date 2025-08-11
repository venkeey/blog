https://chatgpt.com/c/689867f0-d9f8-832e-ad32-cc80971529c8

Goal (short)
PoP should reward useful, measurable contributions (validation, dApp hosting, storage, uptime, identity attestations, relaying, moderation, etc.) rather than raw wealth, while remaining Sybil-resistant, battery-/bandwidth-friendly, and auditable.

1. Define participation classes
Group actions so scoring and verification are simple.

Consensus participation

Block proposal, block validation, attestation, relayer service.

Infrastructure hosting

Subchain host, archive host, indexer, RPC provider, UBC compute provider.

Service contributions

Identity attestation, KYC/Verifications, social moderation, dispute arbitration.

Economic/service activity

Running dApp, serving transactions for micro-payments, liquidity provision in community pools.

Social / governance

Voting, delegate work, proposal authorship, community mentoring.

Each class has an objective metric set (e.g., blocks validated, uptime %, bytes served, attestations signed, votes cast).

2. Participation score: canonical formula (example)
Make a weighted, time-decayed score so recent activity matters.

Let each node/user i have per-class counts c_{i,j}(t) measured over a sliding window (e.g., last 30 days). Define weights w_j for classes (governance vs infra vs consensus).

Participation score (raw):

mathematica
Copy
Edit
raw_i(t) = sum_j w_j * D(c_{i,j}(t))
Where D() is a diminishing returns function to avoid single-action domination, e.g. D(x) = log(1 + x) or D(x) = x^α with 0<α<1.

Time decay: apply exponential decay to older contributions

cpp
Copy
Edit
c_{i,j}(t) = sum_k a_{k} * exp(-(t - t_k)/τ)
Where events k have timestamps t_k, a_k are event weights, and τ is decay constant (e.g., 7–30 days).

Normalize to public scale:

ini
Copy
Edit
participation_score_i = scale( raw_i(t) / (raw_max(t) + ε) ) * MaxScore
MaxScore could be 1000. scale() may be logistic to compress extremes.

Example weights (starting point):

Consensus validation: w = 3.0

Infrastructure hosting (UBC): w = 2.5

Archive / storage serving: w = 2.0

Identity attestation: w = 1.5

Governance voting: w = 1.0

Social moderation: w = 0.8

Tune these weights by policy & simulations.

3. Reward distribution
Link rewards to participation score but include diminishing returns and caps.

Total reward pool R per epoch:

Compute normalized contributions p_i = participation_score_i / sum_k participation_score_k.

Base reward: r_base_i = R * p_i.

Apply fairness cap: r_final_i = min(r_base_i, cap + α * activity_variance_adjustment).

Optionally apply tenure multiplier for new entrants (bonus to bootstrap).

Add small permanent stipend for low-resource participants (UBC): low-bandwidth nodes get periodic top-up to stay online.

4. Sybil resistance & identity
PoP is vulnerable to Sybil attacks; combine multiple defenses.

DID with attestations: Link identities to real-world attestations (email, phone hashed, optional KYC), but preserve privacy via ZK proofs. Requiring some attestations increases cost for attackers.

Costly actions: Some contributions require bonded deposits or demonstration-of-work (very small, e.g., proof-of-storage for a day) to raise Sybil cost.

Reputation accrual: Reputation must grow over time; short bursts of activity give lower weight than sustained contribution.

Social graph heuristics: Use trust graph — endorsements from reputable nodes increase weight; new identities require endorsements.

Rate limits & diminishing returns: D(x)=log(1+x) prevents farming scores by repeating low-value actions.

5. Eligibility / roles / seat model
Define roles with minimum participation to be eligible for validator-like tasks:

Light participants: any device (including phones) that runs a light client and relays; can earn small fraction.

Verified hosts: arc/node hosts with uptime > X% over last Y days, minimum storage & bandwidth.

Validator seats / full nodes: require higher score + stake or multi-party certificate; slotting can be dynamic based on score ranking.

You can have on-chain/off-chain mapping: e.g., top 50 PoP scorers qualify as validators for epoch.

6. Governance & reputation interplay
Connect participation to governance power but avoid plutocracy:

Voting power = f(participation_score, reputation_score). Use sublinear mapping:

ini
Copy
Edit
vote_power = (participation_score)^β * (reputation_score)^γ
With β<1 (e.g., 0.6) to diminish concentration.

Reputation grows via positive audits, time-staked good behavior, verified service milestones; it decays on slashing.

Allow delegation: if user delegates vote to a trusted operator, that operator may exercise votes but delegation must be revocable and visible.

7. Slashing, dispute resolution & anti-capture
If participants misbehave:

Slashing triggers: double-signing, fraudulent attestations, consistent downtime when committed, misreporting.

Proofs required: any slashing must rely on verifiable evidence (logs, signed messages, merkle proofs).

Dispute channel: accused party has a window (e.g., 48–72 hours) to present proof; emergency rollback only with higher quorum.

Gradual penalties: start with reputation decay, remove privileges, then deposit slashing for severe offenses.

Human DAO / governance can override slashing under extraordinary circumstances but every override is public and anchored.

8. Verification & lightweight proofs for phones
Mobile devices must be able to verify actions cheaply:

Threshold signatures (BLS/Schnorr aggregate): aggregate many approvals into one compact proof for the phone to verify.

Merkle proofs for state: phones verify balance/ownership via Merkle root anchored in server/public chain.

ZK proofs for offloaded computation: heavy verification (e.g., fraud checks) can be proven with succinct ZK proofs the phone verifies quickly.

Event push notifications: use push service + small signed proof blob — no heavy sync.

9. Anchoring & audibility
To prevent DAO/server collusion or rollbacks:

Periodically anchor ledger root (or proposal roots) into a public blockchain (e.g., once per hour or per epoch). This gives tamper evidence.

Public audit log with signed proposals and aggregated signatures.

10. Parameter suggestions (starting defaults)
Epoch = 1 day.

Sliding window for score c_{i,j}: 30 days.

Decay τ = 14 days.

D(x) = log(1 + x).

Initial weights: consensus 3.0, infra 2.5, storage 2.0, attestations 1.5, governance 1.0.

Quorum for validator slot assignment: top N by score where N configurable (e.g., 50).

Reward pool split: 70% infra/consensus, 20% governance/community, 10% bootstraps/new entrants.

Tune via simulation.

11. Implementation blueprint (practical)
Event schema: canonicalize event logs (signed JSON) for all participation events.

Collector & aggregator: node-side agent batches and publishes event proofs to aggregator servers or DHT.

Scorer / reputation engine: processes events, applies decay, computes participation_score; expose APIs.

Verifier libraries: SDKs for Android/iOS that verify aggregated sigs, merkle roots, and ZK proofs.

Reward engine: uses scores each epoch to compute and distribute rewards (on-chain or via the DAO-controlled treasury).

Audit + anchor service: create anchor transactions and public feed.

Prefer modular microservices so you can swap D(x), τ, weights without migrating data.

12. Simulation & testing plan
Before mainnet:

Simulate attackers creating 1k–10k Sybils performing low-value actions to test score resistance.

Model honest growth curves and reward distributions; check centralization risk (Gini coefficient of rewards).

Run time-series stress tests with churn (phones on/off), network partitions, and delayed signings.

Security audit for signature aggregation and proposer selection.

13. UX & onboarding (phones)
Make light client plug-and-play: minimal storage, auto-sync only checkpoints, background sync during charging/Wi-Fi.

Provide clear privacy controls: allow participating anonymously with limited services vs. identity-verified high-reward participation.

Show user participation dashboard: score, rewards earned, reputation, recent events.

14. Example: scoring pseudo-code
python
Copy
Edit
# events: list of (timestamp, class_id, amount)
def compute_score(events, now, tau=14*24*3600, weights=WEIGHTS):
    scores = defaultdict(float)
    for ts, cls, amt in events:
        age = (now - ts) / 3600.0
        decay = math.exp(-age / (tau/3600.0))
        scores[cls] += amt * decay
    raw = 0.0
    for cls, val in scores.items():
        raw += weights[cls] * math.log1p(val)  # diminishing returns
    return raw
15. Governance & evolution
PoP rules must be evolvable:

Make scoring parameters themselves subject to governance proposals, requiring higher quorum and time-locks.

Provide fallback defaults and grace periods for parameter changes so participants aren’t blindsided.