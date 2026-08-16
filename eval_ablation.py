import json
from app import app

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

if __name__ == "__main__":
    run_ablation_eval()
