import urllib.request
import csv
import io
import json
import random
import os

# Map dataset Category string directly to close O*NET SOC codes
CATEGORY_SOC_MAP = {
    'Data Science': '15-2051.00',       # Data Scientists
    'HR': '13-1071.00',                 # Human Resources Specialists
    'Advocate': '23-1011.00',           # Lawyers (advocate)
    'Arts': '27-1019.00',               # Artists and Related Workers, All Other
    'Web Designing': '15-1255.00',      # Web and Digital Interface Designers
    'Mechanical Engineer': '17-2141.00', # Mechanical Engineers
    'Sales': '41-3091.00',              # Sales Representatives of Services, Except Advertising, Insurance...
    'Database': '15-1242.00',           # Database Administrators
    'Health and fitness': '39-9031.00',  # Exercise Trainers and Group Fitness Instructors
    'Civil Engineer': '17-2051.00',     # Civil Engineers
    'Java Developer': '15-1252.00',     # Software Developers (Java)
    'Business Analyst': '15-2051.01',   # Business Intelligence Analysts
    'SAP Developer': '15-1252.00',      # Software Developers (SAP)
    'Automation Testing': '15-1253.00', # Software Quality Assurance Analysts and Testers (automation testing)
    'Electrical Engineering': '17-2071.00', # Electrical Engineers
    'Operations Manager': '11-1021.00', # General and Operations Managers
    'Python Developer': '15-1252.00',   # Software Developers (Python)
    'DevOps Engineer': '15-1299.08',    # Computer Systems Engineers/Architects (DevOps)
    'Network Security Engineer': '15-1212.00', # Information Security Analysts
    'PMO': '13-1082.00',                # Project Management Specialists (PMO)
    'Hadoop': '15-2051.00',             # Data Scientists (Hadoop)
    'ETL Developer': '15-2051.01',      # Business Intelligence Analysts (ETL)
    'DotNet Developer': '15-1252.00',   # Software Developers (.Net)
    'Blockchain': '15-1299.07',         # Blockchain Engineers (Blockchain)
    'Testing': '15-1253.00'             # Software Quality Assurance Analysts and Testers (testing)
}

# Derived lexicons for RIASEC dimensions from resume text
RIASEC_LEXICON = {
    'R': ['mechanical', 'electrical', 'hardware', 'network', 'installation', 'assembly', 'manual', 'technician', 'civil', 'wiring', 'maintenance', 'operations', 'repairs', 'tools', 'routing'],
    'I': ['programming', 'developer', 'analysis', 'data', 'scientist', 'python', 'algorithm', 'research', 'mathematics', 'statistics', 'code', 'analytics', 'machine-learning', 'database', 'java', 'sql', 'software'],
    'A': ['design', 'creative', 'ui', 'ux', 'figma', 'artistic', 'graphic', 'writer', 'author', 'content', 'media', 'photography', 'branding', 'video', 'editing', 'style', 'layout'],
    'S': ['support', 'helper', 'service', 'community', 'teaching', 'training', 'customer-success', 'team', 'team-player', 'collaborate', 'mentor', 'recruiting', 'counseling', 'communication', 'human-resources', 'client'],
    'E': ['sales', 'manager', 'product', 'lead', 'marketing', 'growth', 'business', 'strategy', 'consulting', 'planning', 'presentation', 'entrepreneur', 'executive', 'finance', 'agile', 'scrum', 'budget'],
    'C': ['admin', 'organizer', 'process', 'database-administrator', 'records', 'database-management', 'office', 'audit', 'billing', 'compliance', 'documentation', 'conventional', 'inventory', 'excel', 'structure']
}

def derive_riasec_scores(text):
    text_lower = text.lower()
    counts = {dim: 1.0 for dim in ['R', 'I', 'A', 'S', 'E', 'C']}
    for dim, keywords in RIASEC_LEXICON.items():
        for kw in keywords:
            counts[dim] += text_lower.count(kw)
            
    # Rescale vector to [0, 10] range
    max_val = max(counts.values())
    min_val = min(counts.values())
    
    rescaled = {}
    if max_val > min_val:
        for dim in counts:
            rescaled[dim] = round((counts[dim] - min_val) / (max_val - min_val) * 10.0, 2)
    else:
        for dim in counts:
            rescaled[dim] = 5.0
            
    return rescaled

def build_dataset():
    print("Step 1: Downloading raw resume dataset...")
    url = 'https://raw.githubusercontent.com/611noorsaeed/Resume-Screening-App/main/UpdatedResumeDataSet.csv'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return
        
    reader = csv.reader(io.StringIO(content))
    next(reader) # skip header
    
    raw_rows = list(reader)
    print(f"Downloaded {len(raw_rows)} total rows.")
    
    processed_examples = []
    skipped_count = 0
    
    for idx, row in enumerate(raw_rows):
        if len(row) < 2:
            skipped_count += 1
            continue
            
        category = row[0].strip()
        resume_text = row[1].strip()
        
        # Map Category to SOC
        soc_code = CATEGORY_SOC_MAP.get(category)
        if not soc_code:
            skipped_count += 1
            continue
            
        # Derive RIASEC scores
        derived_riasec = derive_riasec_scores(resume_text)
        
        # Add metadata features to emulate user selections
        # For realistic modeling, let's randomly assign some preferences
        # but keep it deterministic by seeding
        random.seed(idx)
        
        # Let's derive primary drivers/likes/flexibility naturally or semi-randomly
        drivers = ['Passion', 'Money', 'Growth', 'Impact', 'Balance']
        driver = random.choice(drivers)
        
        flexibilities = ['Low', 'Medium', 'High']
        flexibility = random.choice(flexibilities)
        
        # Generate some likes based on derived high-interest categories
        # UX Designer gets ui-ux figma, Developer gets coding, HR gets recruiting
        likes = []
        if 'design' in resume_text.lower():
            likes.append('ui-ux')
        if 'figma' in resume_text.lower():
            likes.append('graphic-design')
        if 'data' in resume_text.lower():
            likes.append('machine-learning')
        if 'developer' in resume_text.lower():
            likes.append('python')
            
        processed_examples.append({
            "id": idx,
            "category": category,
            "soc_code": soc_code,
            "riasec": derived_riasec,
            "likes": likes,
            "dislikes": [],
            "intent": "Full-time",
            "driver": driver,
            "financial_flexibility": flexibility
        })
        
    print(f"Processed {len(processed_examples)} examples. Skipped: {skipped_count}")
    
    # 80/20 train/test split (shuffle with seed 42)
    random.seed(42)
    random.shuffle(processed_examples)
    
    split_idx = int(len(processed_examples) * 0.8)
    train_set = processed_examples[:split_idx]
    test_set = processed_examples[split_idx:]
    
    print(f"Train Set Size: {len(train_set)}")
    print(f"Test Set Size: {len(test_set)}")
    
    # Save datasets to disk
    os.makedirs("onet_data", exist_ok=True)
    with open("onet_data/resume_train_set.json", "w") as f:
        json.dump(train_set, f, indent=2)
    with open("onet_data/resume_test_set.json", "w") as f:
        json.dump(test_set, f, indent=2)
        
    print("Successfully saved train and test datasets to onet_data/ folder.")
    
    # Print sample distribution
    cat_counts = {}
    for ex in processed_examples:
        cat_counts[ex["category"]] = cat_counts.get(ex["category"], 0) + 1
    print("\nProcessed category distribution:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} (mapped to SOC: {CATEGORY_SOC_MAP[cat]})")

if __name__ == "__main__":
    build_dataset()
