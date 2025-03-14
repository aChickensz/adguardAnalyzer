import json
from collections import Counter, defaultdict
import tldextract

# Load JSON file
with open("adguard_queries.json", "r") as f:
    raw = json.load(f)

queries = raw["data"]

# Track domain hits and which IPs made them
domain_counts = Counter()
nosub_counts = Counter()
domain_by_ip = defaultdict(lambda: Counter())
nosub_by_ip = defaultdict(lambda: Counter())
def get_base_domain(domain):
    extracted = tldextract.extract(domain)
    return f"{extracted.domain}.{extracted.suffix}"

for q in queries:
    question = q.get("question")
    domain = question.get("name") if isinstance(question, dict) else "unknown"
    ip = q.get("client", "unknown")
    no_subdomain = get_base_domain(domain)
    domain_counts[domain] += 1
    nosub_counts[no_subdomain] += 1
    domain_by_ip[ip][domain] += 1
    nosub_by_ip[ip][domain] += 1

# Display top 10 most queried domains overall
print("Top 10 Queried Domains:")
for domain, count in domain_counts.most_common(10):
    print(f"{domain}: {count} requests")

# Show top 5 domains per client IP
print("\nTop Queried Domains Per IP:")
for ip, domains in domain_by_ip.items():
    print(f"\n{ip}:")
    for domain, count in domains.most_common(5):
        print(f"  {domain}: {count}x")

print("\n\n-------------------------------------\n\n")
print("Top 10 Queried Domains without Subdomain:")

for domain, count in nosub_counts.most_common(10):
    print(f"{domain}: {count} requests")

print("\nTop Queried Domains Per IP without Subdomain:")
for ip, domains in nosub_by_ip.items():
    print(f"\n{ip}:")
    for domain, count in domains.most_common(5):
        print(f"  {domain}: {count}x")
