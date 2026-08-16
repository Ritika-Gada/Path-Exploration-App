import json
import math
from app import app, load_onet_data
from train_model import get_career_riasec_and_tags, compute_features

def run_ablation_eval():
    print("=" * 90)
    print("PATHFINDER MATCHING ENGINE - ABLATION EVALUATION STUDY")
    print("=" * 90)
    
    # Define 5 distinct user profiles targeting different dominant RIASEC traits
    profiles = [
        {
            "name": "Investigative Tech Leader (Data/AI focus)",
            "payload": {
                "riasec": {"R": 3, "I": 9, "A": 5, "S": 2, "E": 7, "C": 4},
                "likes": ["machine-learning", "python", "cloud-computing"],
                "dislikes": ["sales", "cold-calling"],
                "intent": "Full-time",
                "current_role": "Professional",
                "driver": "Growth",
                "financial_flexibility": "High",
                "self_judgement": {"creativity": 6, "analytical": 9, "social": 5}
            }
        },
        {
            "name": "Artistic Creator & Designer",
            "payload": {
                "riasec": {"R": 1, "I": 3, "A": 10, "S": 5, "E": 4, "C": 2},
                "likes": ["ui-ux", "graphic-design", "figma"],
                "dislikes": ["backend-dev", "database-management"],
                "intent": "Full-time",
                "current_role": "Student",
                "driver": "Passion",
                "financial_flexibility": "Medium",
                "self_judgement": {"creativity": 10, "analytical": 3, "social": 6}
            }
        },
        {
            "name": "Low-Resource Hobbyist (Realistic/Conventional)",
            "payload": {
                "riasec": {"R": 8, "I": 4, "A": 2, "S": 1, "E": 3, "C": 8},
                "likes": ["robotics", "hardware", "iot"],
                "dislikes": [],
                "intent": "Hobby",
                "current_role": "Student",
                "driver": "Side Hustle",
                "financial_flexibility": "Low", # Low budget -> high barrier penalty, low barrier boost
                "self_judgement": {"creativity": 3, "analytical": 6, "social": 2}
            }
        },
        {
            "name": "Social/Enterprising People Manager",
            "payload": {
                "riasec": {"R": 1, "I": 4, "A": 5, "S": 9, "E": 9, "C": 4},
                "likes": ["agile-coaching", "scrum", "public-relations"],
                "dislikes": ["assembly-programming"],
                "intent": "Full-time",
                "current_role": "Professional",
                "driver": "Impact",
                "financial_flexibility": "Medium",
                "self_judgement": {"creativity": 7, "analytical": 5, "social": 9}
            }
        },
        {
            "name": "Conventional & FinTech Specialist",
            "payload": {
                "riasec": {"R": 2, "I": 5, "A": 2, "S": 4, "E": 7, "C": 9},
                "likes": ["personal-finance", "excel", "blockchain"],
                "dislikes": ["artistic-painting"],
                "intent": "Full-time",
                "current_role": "Professional",
                "driver": "Wealth",
                "financial_flexibility": "High",
                "self_judgement": {"creativity": 3, "analytical": 8, "social": 6}
            }
        }
    ]
    
    client = app.test_client()
    
    for prof in profiles:
        print(f"\nProfile: {prof['name']}")
        print("-" * 90)
        print(f"User RIASEC: {prof['payload']['riasec']}")
        print(f"Likes: {prof['payload']['likes']} | Dislikes: {prof['payload']['dislikes']}")
        print(f"Driver: {prof['payload']['driver']} | Financial Flexibility: {prof['payload']['financial_flexibility']}")
        print("-" * 90)
        
        response = client.post('/api/match', 
                               data=json.dumps(prof['payload']),
                               content_type='application/json')
        res_data = json.loads(response.data)
        
        # Display top 5 matches with component ablation details
        print(f"{'Top Curated Career':<32} | {'Base Match':<10} | {'Tag Bonus':<9} | {'Driver B.':<9} | {'Barrier Adj':<11} | {'Final Score':<11}")
        print("-" * 90)
        
        for idx, match in enumerate(res_data['results'][:5]):
            print(f"{match['name']:<32} | "
                  f"{match['base_score']:<10} | "
                  f"{match['tag_bonus']:<9} | "
                  f"{match['driver_bonus']:<9} | "
                  f"{match['barrier_adjustment']:<11} | "
                  f"{match['final_score']:<11}")
            
        # Display secondary results if any
        sec_results = res_data.get('secondary_results', [])
        if sec_results:
            print("\n  >> Alternate Exploring Recommendations (Score higher than top curated):")
            for sr in sec_results:
                print(f"     * [{sr['soc_code']}] {sr['title']} (Base Match Score: {sr['score']}%)")
        else:
            print("\n  >> Alternate Exploring Recommendations: None scored higher than top curated.")
        print("=" * 90)

def run_model_comparison_eval():
    print("\n" + "=" * 90)
    print("HEURISTIC VS TRAINED ML MODEL COMPARISON STUDY")
    print("=" * 90)
    
    # 1. Load O*NET database
    try:
        onet_db = load_onet_data()
    except Exception as e:
        print(f"Error loading O*NET database: {e}")
        return
        
    # 2. Load trained coefficients
    try:
        with open("onet_data/model_coefficients.json", "r") as f:
            coefs = json.load(f)
        intercept = coefs["intercept"]
        coef_riasec = coefs["coef_riasec_similarity"]
        coef_tag = coefs["coef_tag_overlap"]
        mean_riasec = coefs["mean_riasec_similarity"]
        mean_tag = coefs["mean_tag_overlap"]
        std_riasec = coefs["std_riasec_similarity"]
        std_tag = coefs["std_tag_overlap"]
    except Exception as e:
        print(f"Error loading model coefficients: {e}")
        return
        
    # 3. Load held-out test set
    try:
        with open("onet_data/resume_test_set.json", "r") as f:
            test_set = json.load(f)
    except Exception as e:
        print(f"Error loading test set: {e}")
        return
        
    heuristic_top5_hits = 0
    heuristic_top10_hits = 0
    model_top5_hits = 0
    model_top10_hits = 0
    
    # Store binary correctness arrays for McNemar's paired test
    h_top5_correct = []
    m_top5_correct = []
    
    all_socs = list(onet_db.keys())
    
    for ex in test_set:
        user_riasec = ex["riasec"]
        user_likes = ex["likes"]
        target_soc = ex["soc_code"]
        
        heuristic_scores = []
        model_scores = []
        
        for soc in all_socs:
            career_riasec, career_tags = get_career_riasec_and_tags(soc, onet_db)
            if career_riasec is None:
                continue
                
            feats = compute_features(user_riasec, user_likes, career_riasec, career_tags)
            riasec_sim, tag_overlap = feats[0], feats[1]
            
            # Heuristic score calculation
            h_score = riasec_sim + (4.0 * tag_overlap)
            heuristic_scores.append((soc, h_score))
            
            # Z-standardized ML Model score calculation (logistic probability rescaled to 0-100)
            riasec_sim_scaled = (riasec_sim - mean_riasec) / std_riasec
            tag_overlap_scaled = (tag_overlap - mean_tag) / std_tag
            logit = intercept + (coef_riasec * riasec_sim_scaled) + (coef_tag * tag_overlap_scaled)
            prob = 1.0 / (1.0 + math.exp(-logit))
            m_score = prob * 100.0
            model_scores.append((soc, m_score))
            
        heuristic_scores.sort(key=lambda x: x[1], reverse=True)
        model_scores.sort(key=lambda x: x[1], reverse=True)
        
        heuristic_ranks = [x[0] for x in heuristic_scores]
        model_ranks = [x[0] for x in model_scores]
        
        h_hit_top5 = target_soc in heuristic_ranks[:5]
        m_hit_top5 = target_soc in model_ranks[:5]
        h_top5_correct.append(h_hit_top5)
        m_top5_correct.append(m_hit_top5)
        
        if h_hit_top5:
            heuristic_top5_hits += 1
        if target_soc in heuristic_ranks[:10]:
            heuristic_top10_hits += 1
            
        if m_hit_top5:
            model_top5_hits += 1
        if target_soc in model_ranks[:10]:
            model_top10_hits += 1
            
    total_test = len(test_set)
    heuristic_top5_acc = (heuristic_top5_hits / total_test) * 100.0
    heuristic_top10_acc = (heuristic_top10_hits / total_test) * 100.0
    model_top5_acc = (model_top5_hits / total_test) * 100.0
    model_top10_acc = (model_top10_hits / total_test) * 100.0
    
    # Calculate McNemar Contingency Table
    both_correct = 0
    model_only = 0
    heuristic_only = 0
    both_incorrect = 0
    
    for h_correct, m_correct in zip(h_top5_correct, m_top5_correct):
        if h_correct and m_correct:
            both_correct += 1
        elif not h_correct and m_correct:
            model_only += 1      # cell b
        elif h_correct and not m_correct:
            heuristic_only += 1  # cell c
        else:
            both_incorrect += 1
            
    # Calculate McNemar exact binomial p-value (since b + c is small)
    n_disagreements = model_only + heuristic_only
    p_value = 1.0
    if n_disagreements > 0:
        k = min(model_only, heuristic_only)
        binomial_sum = 0.0
        for i in range(k + 1):
            binomial_sum += math.comb(n_disagreements, i) * (0.5 ** n_disagreements)
        p_value = min(1.0, binomial_sum * 2.0)
    
    print(f"Test Set Size: {total_test} profiles")
    print(f"Candidate Pool Size: {len(all_socs)} occupations")
    print(f"Random Chance (Top-5): {(5.0 / len(all_socs)) * 100.0:.3f}%")
    print(f"Random Chance (Top-10): {(10.0 / len(all_socs)) * 100.0:.3f}%")
    print("-" * 90)
    print(f"Metric      | Heuristic Weights | Trained ML Model | Lift")
    print("-" * 90)
    print(f"Top-5 Acc   | {heuristic_top5_acc:16.2f}% | {model_top5_acc:15.2f}% | {model_top5_acc - heuristic_top5_acc:+.2f}%")
    print(f"Top-10 Acc  | {heuristic_top10_acc:16.2f}% | {model_top10_acc:15.2f}% | {model_top10_acc - heuristic_top10_acc:+.2f}%")
    print("-" * 90)
    print("Statistical Significance (Top-5 hits):")
    print(f"  Both Correct: {both_correct} | Both Incorrect: {both_incorrect}")
    print(f"  Model Correct Only (b): {model_only} | Heuristic Correct Only (c): {heuristic_only}")
    print(f"  McNemar paired exact p-value: {p_value:.4f}")
    if p_value < 0.05:
        print("  Result: The model lift is STATISTICALLY SIGNIFICANT (p < 0.05).")
    else:
        print("  Result: The model lift is NOT statistically significant (p >= 0.05).")
    print("=" * 90)

if __name__ == "__main__":
    run_ablation_eval()
    run_model_comparison_eval()
