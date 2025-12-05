import csv
import os
import time
import math
#load data 
def load_data(path="uni.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    records = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'id': int(row['id']),
                'name': row['name'],
                'major': row['major']
            })
    return records

records = load_data("uni.csv")
print(f"Loaded {len(records)} records.")


class PrimaryIndex:
    def __init__(self, records, block_size=100):
        self.block_size = block_size
        self.records = sorted(records, key=lambda r:r['id'])#sort based on id
        self.index = []

    def build(self):
        n = len(self.records)#total number of records

        for block in range(math.ceil(n / self.block_size)):
            id = self.records[block * self.block_size]['id']
            self.index.append((id, block))
        
    def exact_match(self, key):
        ids = []
        for id, blocknum in self.index:
            ids.append(id)

        #########################binary search
        lo, hi = 0, len(ids)-1
        block_num = 0
        while lo <= hi:
            mid = (lo + hi)//2
            if ids[mid] == key:
                block_num = self.index[mid][1]
                break
            elif ids[mid] < key:
                block_num = self.index[mid][1]
                lo = mid + 1
            else:
                hi = mid - 1
        ###########################
        start = block_num * self.block_size
        block = self.records[start:start + self.block_size]

        for rec in block:
            if rec['id'] == key:
                return rec, 1 + 1
        return None, 1 + 1
    
    
    def range_query(self, low, high):
        ids = []
        for id, blocknum in self.index:
            ids.append(id)

        ########################
        lo, hi = 0, len(ids)-1
        block_idx = 0
        while lo <= hi:
            mid = (lo + hi)//2
            if ids[mid] < low:
                block_idx = mid
                lo = mid + 1
            else:
                hi = mid - 1

        #####################
        blocks = 0
        results = []
        for _, block_num in self.index[block_idx:]:
            blocks += 1
            start = block_num * self.block_size
            block = self.records[start:start + self.block_size]
            for r in block:
                if low <= r['id'] <= high:
                    results.append(r)
                elif r['id'] > high:
                    return results, 1 + blocks
        return results, 1 + blocks
    

class ClusteringIndex:
    def __init__(self, records, block_size=100):
        self.block_size = block_size
        self.records = sorted(records, key=lambda r: r['major'])
        self.index = {} 

    def build(self):
        n = len(self.records)
        for block in range((math.ceil(n/self.block_size))):
            start = block * self.block_size
            value = self.records[start]['major']
            if value not in self.index:
                self.index[value] = block
            
    def exact_match(self, value):
        if value not in self.index:
            return[], 0
        block = self.index[value]
        start = block * self.block_size
        block = self.records[start:start + self.block_size]
        results = []
        for r in block:
            if r['major'] == value:
                results.append(r)
        return results, 1


    




# === Cell 5 — Benchmark: File Scan vs Indexes (time + block counts) ===
import time

BLOCK_SIZE = 100  # keep consistent with your index classes

def file_exact_search(records, field, value, block_size=BLOCK_SIZE):
    """Linear scan for exact match on any field."""
    blocks, results = 0, []
    n = len(records)
    for blk in range((n + block_size - 1)//block_size):
        blocks += 1
        chunk = records[blk*block_size:(blk+1)*block_size]
        for r in chunk:
            if r[field] == value:
                results.append(r)
    return results, blocks


def file_exact_search_id_first(records, key, block_size=BLOCK_SIZE):
    """Binary search for id in a sorted file."""
    blocks = 0
    n = len(records)

    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2

        # Access the block containing 'mid'
        blocks += 1
        blk_start = (mid // block_size) * block_size
        blk_end = blk_start + block_size
        chunk = records[blk_start:blk_end]

        # Search inside the block
        for r in chunk:
            if r['id'] == key:
                return r, blocks

        # Move binary search boundaries
        if records[mid]['id'] < key:
            lo = mid + 1
        else:
            hi = mid - 1

    return None, blocks


def file_range_search_id(records, low, high, block_size=BLOCK_SIZE):
    """Range search on sorted file by id (binary search start, then sequential scan)."""
    blocks = 0
    results = []
    n = len(records)

    # --- Find first position >= low using binary search ---
    lo, hi = 0, n - 1
    start_pos = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if records[mid]['id'] < low:
            lo = mid + 1
        else:
            start_pos = mid
            hi = mid - 1

    if start_pos is None:
        return [], 0  # no records >= low

    # --- Sequentially read blocks until id > high ---
    pos = start_pos
    while pos < n and records[pos]['id'] <= high:
        blk_start = (pos // block_size) * block_size
        blk_end = blk_start + block_size
        blocks += 1

        chunk = records[blk_start:blk_end]
        for r in chunk:
            if low <= r['id'] <= high:
                results.append(r)
            elif r['id'] > high:
                return results, blocks  # stop early
        pos = blk_end  # jump to next block

    return results, blocks
# --------- Build indexes (fresh) ---------
pi = PrimaryIndex(records, block_size=BLOCK_SIZE);  pi.build()
ci = ClusteringIndex(records, block_size=BLOCK_SIZE); ci.build()
# si_name = SecondaryIndex(records, block_size=BLOCK_SIZE, field='name'); si_name.build()

# --------- Pick reproducible test keys ---------
mid = len(records)//2
test_id    = records[mid]['id']
test_major = records[mid//3]['major']
test_name  = records[mid//4]['name']
low, high  = test_id - 50, test_id + 50

# --------- Run comparisons ---------
rows = []

# A) Exact by ID: file vs primary index
t0 = time.perf_counter(); _, blk_fs = file_exact_search_id_first(records, test_id); dt_fs = (time.perf_counter()-t0)*1000
t0 = time.perf_counter(); _, blk_pi = pi.exact_match(test_id);                    dt_pi = (time.perf_counter()-t0)*1000
rows.append(["Exact by ID", f"id={test_id}", "File scan", blk_fs, f"{dt_fs:.6f}"])
rows.append(["Exact by ID", f"id={test_id}", "Primary index", blk_pi, f"{dt_pi:.6f}"])

# B) Range by ID: file vs primary index
t0 = time.perf_counter(); res_fr, blk_fr = file_range_search_id(records, low, high); dt_fr = (time.perf_counter()-t0)*1000
t0 = time.perf_counter(); res_pr, blk_pr = pi.range_query(low, high);               dt_pr = (time.perf_counter()-t0)*1000
rows.append(["Range by ID", f"{low}..{high}", "File scan", blk_fr, f"{dt_fr:.6f}"])
rows.append(["Range by ID", f"{low}..{high}", "Primary index", blk_pr, f"{dt_pr:.6f}"])


# C) Exact by Major: file vs clustering index
t0 = time.time(); _, blk_fm = file_exact_search(records, 'major', test_major); dt_fm = (time.time()-t0)*1000
t0 = time.time(); _, blk_cm = ci.exact_match(test_major);                     dt_cm = (time.time()-t0)*1000
rows.append(["Exact by Major", f"major='{test_major}'", "File scan", blk_fm, f"{dt_fm:.3f}"])
rows.append(["Exact by Major", f"major='{test_major}'", "Clustering index", blk_cm, f"{dt_cm:.3f}"])

# # D) Exact by Name: file vs secondary index on name
# t0 = time.time(); _, blk_fn = file_exact_search(records, 'name', test_name); dt_fn = (time.time()-t0)*1000
# t0 = time.time(); _, blk_sn = si_name.exact_match(test_name);               dt_sn = (time.time()-t0)*1000
# rows.append(["Exact by Name", f"name='{test_name}'", "File scan", blk_fn, f"{dt_fn:.3f}"])
# rows.append(["Exact by Name", f"name='{test_name}'", "Secondary index (name)", blk_sn, f"{dt_sn:.3f}"])

# --------- Pretty print table ---------
headers = ["Query Type", "Key", "Method", "Blocks", "Time (ms)"]
colw = [max(len(str(x)) for x in ([h] + [r[i] for r in rows])) for i,h in enumerate(headers)]
fmt = "  ".join("{:<" + str(w) + "}" for w in colw)

print(fmt.format(*headers))
print("-" * (sum(colw) + 2*(len(headers)-1) + 2))
for r in rows:
    print(fmt.format(*r))
