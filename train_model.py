import json
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from app import CAREERS_DB, CURATED_SOC_MAPPING, load_onet_data

def get_career_riasec_and_tags(soc_code, onet_db):
    # Check if curated
    curated_career = None
    for c in CAREERS_DB:
        # Check by mapped SOC code
        if CURATED_SOC_MAPPING.get(c["id"]) == soc_code:
            curated_career = c
            break
            
    if curated_career:
        return curated_career["riasec"], curated_career["tags"]
    elif soc_code in onet_db:
        return onet_db[soc_code]["riasec"], []
    else:
        return None, []

def compute_features(user_riasec, user_likes, career_riasec, career_tags):
    # 1. RIASEC similarity (100 - Manhattan Distance normalized to percentage)
    total_dist = 0.0
    dimensions = ["R", "I", "A", "S", "E", "C"]
    for dim in dimensions:
        u_val = user_riasec.get(dim, 5.0)
        c_val = career_riasec.get(dim, 5.0)
        total_dist += abs(u_val - c_val)
    riasec_similarity = (1.0 - (total_dist / 60.0)) * 100.0
    
    # 2. Tag overlap count
    tag_overlap = 0.0
    for tag in user_likes:
        if tag in career_tags:
            tag_overlap += 1.0
            
    return [riasec_similarity, tag_overlap]

def prepare_dataset(split_file, onet_db, random_seed):
    random.seed(random_seed)
    with open(split_file, "r") as f:
        examples = json.load(f)
        
    X = []
    y = []
    
    # Pre-split curated SOC codes and wider O*NET SOC codes
    curated_socs = list(CURATED_SOC_MAPPING.values())
    all_socs = list(onet_db.keys())
    wider_socs = [s for s in all_socs if s not in curated_socs]
    
    for ex in examples:
        user_riasec = ex["riasec"]
        user_likes = ex["likes"]
        pos_soc = ex["soc_code"]
        
        # Positive pair
        pos_riasec, pos_tags = get_career_riasec_and_tags(pos_soc, onet_db)
        if pos_riasec is None:
            continue
        pos_features = compute_features(user_riasec, user_likes, pos_riasec, pos_tags)
        X.append(pos_features)
        y.append(1)
        
        # Negative sampling (5 curated negatives + 10 wider pool negatives)
        # Sample curated negatives
        neg_curated_socs = [s for s in curated_socs if s != pos_soc]
        sampled_curated = random.sample(neg_curated_socs, min(5, len(neg_curated_socs)))
        for neg_soc in sampled_curated:
            neg_riasec, neg_tags = get_career_riasec_and_tags(neg_soc, onet_db)
            neg_features = compute_features(user_riasec, user_likes, neg_riasec, neg_tags)
            X.append(neg_features)
            y.append(0)
            
        # Sample wider pool negatives
        neg_wider_socs = [s for s in wider_socs if s != pos_soc]
        sampled_wider = random.sample(neg_wider_socs, 10)
        for neg_soc in sampled_wider:
            neg_riasec, neg_tags = get_career_riasec_and_tags(neg_soc, onet_db)
            neg_features = compute_features(user_riasec, user_likes, neg_riasec, neg_tags)
            X.append(neg_features)
            y.append(0)
            
    return np.array(X), np.array(y)

def train_pipeline():
    print("Step 2: Training ML matching model using logistic regression...")
    
    # Load database
    try:
        onet_db = load_onet_data()
    except Exception as e:
        print(f"Error loading O*NET database: {e}")
        return
        
    # Prepare datasets
    X_train, y_train = prepare_dataset("onet_data/resume_train_set.json", onet_db, random_seed=42)
    X_test, y_test = prepare_dataset("onet_data/resume_test_set.json", onet_db, random_seed=100)
    
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    
    # Train Logistic Regression
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    
    # Print learned coefficients
    intercept = float(clf.intercept_[0])
    coef_riasec = float(clf.coef_[0][0])
    coef_tag_overlap = float(clf.coef_[0][1])
    
    print("\nLearned Model Coefficients:")
    print(f"  Intercept: {intercept:.4f}")
    print(f"  RIASEC Similarity Coef: {coef_riasec:.4f}")
    print(f"  Tag Overlap Coef: {coef_tag_overlap:.4f}")
    
    # Express as weights relative to RIASEC similarity
    if coef_riasec != 0:
        relative_tag_weight = coef_tag_overlap / coef_riasec
        print(f"\nExplainable Finding: The model learned that 1 matching tag is equivalent to "
              f"+{relative_tag_weight:.2f}% of RIASEC similarity score in matching probability.")
              
    # Save coefficients as JSON for transparency
    coefs = {
        "intercept": intercept,
        "coef_riasec_similarity": coef_riasec,
        "coef_tag_overlap": coef_tag_overlap
    }
    with open("onet_data/model_coefficients.json", "w") as f:
        json.dump(coefs, f, indent=2)
    print("Saved model coefficients to onet_data/model_coefficients.json")
    
    # Verify training accuracy
    train_acc = clf.score(X_train, y_train) * 100.0
    test_acc = clf.score(X_test, y_test) * 100.0
    print(f"Training Accuracy: {train_acc:.2f}%")
    print(f"Testing Accuracy: {test_acc:.2f}%")

if __name__ == "__main__":
    train_pipeline()
