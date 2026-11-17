#B1---------
def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    # TODO: intoarce lista de (ip, n) cu n >= prag,
    #       sortata descrescator dupa n
    return [(ip,n) for ip,n in counts.most_common() if n >= prag]
        

 
from collections import Counter
c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
print(suspecti(c))
print(suspecti(c, prag=2))