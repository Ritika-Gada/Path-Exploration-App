import sys
import unittest
import json
from app import app, CAREERS_DB

class TestCareerMatchPhase2(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_financial_constraints(self):
        # High barrier roles (like MLOps) should get penalized when financial flexibility is Low
        payload_low = {
            "riasec": {"R": 9, "I": 9, "A": 9, "S": 9, "E": 9, "C": 9},
            "likes": [],
            "dislikes": [],
            "intent": "Full-time",
            "current_role": "Student",
            "driver": "Money",
            "financial_flexibility": "Low"
        }
        response_low = self.app.post('/api/match', 
                                     data=json.dumps(payload_low),
                                     content_type='application/json')
        data_low = json.loads(response_low.data.decode('utf-8'))
        
        # High barrier roles should be penalized, check score difference
        mlops_low = next(c for c in data_low["results"] if c["id"] == "mlops_specialist")
        
        payload_high = payload_low.copy()
        payload_high["financial_flexibility"] = "High"
        
        response_high = self.app.post('/api/match', 
                                      data=json.dumps(payload_high),
                                      content_type='application/json')
        data_high = json.loads(response_high.data.decode('utf-8'))
        mlops_high = next(c for c in data_high["results"] if c["id"] == "mlops_specialist")

        # Assertion: high flexibility should score higher than low flexibility for high-barrier role
        self.assertGreater(mlops_high["score"], mlops_low["score"])
        # Penalty is -15% for Low, bonus is +5% for High -> diff should be exactly 20.0
        self.assertEqual(round(mlops_high["score"] - mlops_low["score"], 1), 20.0)
        print("Success: Low financial flexibility correctly penalizes high-barrier roles.")

    def test_milestones_and_quizzes_present(self):
        payload = {
            "riasec": {"R": 5, "I": 5, "A": 5, "S": 5, "E": 5, "C": 5},
            "likes": [],
            "dislikes": [],
            "intent": "Full-time",
            "current_role": "Student",
            "driver": "Passion",
            "financial_flexibility": "Medium"
        }
        response = self.app.post('/api/match', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        
        for career in data["results"]:
            self.assertIn("milestones", career)
            self.assertGreater(len(career["milestones"]), 0)
            
            # Verify structure of first milestone
            first_milestone = career["milestones"][0]
            self.assertIn("id", first_milestone)
            self.assertIn("title", first_milestone)
            self.assertIn("description", first_milestone)
            self.assertIn("quiz", first_milestone)
            self.assertIn("questions", first_milestone["quiz"])
            self.assertGreater(len(first_milestone["quiz"]["questions"]), 0)
            
        print("Success: All matched careers include sequential milestones and structured quiz questions.")

    def test_self_judgement_alignment(self):
        # We define a payload where computed RIASEC traits are:
        # R=2, I=8, A=8, S=2, E=2, C=8
        # Therefore:
        # computed_creativity = (A + R) / 2 = (8 + 2) / 2 = 5.0
        # computed_analytical = (I + C) / 2 = (8 + 8) / 2 = 8.0
        # computed_social = (S + E) / 2 = (2 + 2) / 2 = 2.0
        
        # Scenario A: Self-judgement matches computed traits exactly
        payload_perfect = {
            "riasec": {"R": 2, "I": 8, "A": 8, "S": 2, "E": 2, "C": 8},
            "self_judgement": {"creativity": 5.0, "analytical": 8.0, "social": 2.0},
            "transparency": True,
            "likes": [],
            "dislikes": [],
            "intent": "Full-time",
            "current_role": "Student",
            "driver": "Passion",
            "financial_flexibility": "Medium"
        }
        response = self.app.post('/api/match', 
                                 data=json.dumps(payload_perfect),
                                 content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        
        # Perfect alignment should return 100%
        self.assertEqual(data["alignment_percentage"], 100.0)
        self.assertEqual(data["transparency"], True)
        
        # Scenario B: Self-judgement has differences
        # self_creativity = 8.0 (diff = |8.0 - 5.0| = 3.0)
        # self_analytical = 5.0 (diff = |5.0 - 8.0| = 3.0)
        # self_social = 5.0 (diff = |5.0 - 2.0| = 3.0)
        # Total diff = 9.0
        # alignment_pct = (1.0 - (9.0 / 30.0)) * 100.0 = 70.0%
        payload_diff = payload_perfect.copy()
        payload_diff["self_judgement"] = {"creativity": 8.0, "analytical": 5.0, "social": 5.0}
        payload_diff["transparency"] = False
        
        response_diff = self.app.post('/api/match', 
                                      data=json.dumps(payload_diff),
                                      content_type='application/json')
        data_diff = json.loads(response_diff.data.decode('utf-8'))
        
        self.assertEqual(data_diff["alignment_percentage"], 70.0)
        self.assertEqual(data_diff["transparency"], False)
        print("Success: Self-judgement alignment percentage is calculated accurately and respects transparency status.")

    def test_skipped_questions_safety(self):
        # In a skipped question scenario, some RIASEC dimensions are null
        payload_skipped = {
            "riasec": {
                "R": 5.0,
                "I": None,      # Skipped
                "A": 8.0,
                "S": None,      # Skipped
                "E": 2.0,
                "C": 5.0
            },
            "self_judgement": {
                "creativity": 6.5,
                "analytical": 5.0,
                "social": 2.0
            },
            "transparency": True,
            "likes": [],
            "dislikes": [],
            "intent": "Full-time",
            "current_role": "Student",
            "driver": "Passion",
            "financial_flexibility": "Medium"
        }
        
        response = self.app.post('/api/match', 
                                 data=json.dumps(payload_skipped),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data["success"])
        
        # Check alignment score calculates without raising TypeError
        self.assertIn("alignment_percentage", data)
        self.assertGreaterEqual(data["alignment_percentage"], 0.0)
        self.assertLessEqual(data["alignment_percentage"], 100.0)
        print("Success: Backend matching route handles skipped questions (null inputs) safely and computes normalized scores.")

    def test_onet_overrides_and_score_breakdowns(self):
        # 1. Verify CAREERS_DB has overwritten RIASEC values
        for career in CAREERS_DB:
            self.assertIn("original_riasec", career)
            self.assertIn("onet_soc_code", career)
            self.assertNotEqual(career["riasec"], career["original_riasec"])

        # 2. Verify score breakdowns in API response
        payload = {
            "riasec": {"R": 6, "I": 8, "A": 4, "S": 2, "E": 6, "C": 8},
            "likes": ["machine-learning", "python"],
            "dislikes": [],
            "intent": "Full-time",
            "current_role": "Student",
            "driver": "Growth",
            "financial_flexibility": "Low",
            "self_judgement": {"creativity": 5, "analytical": 8, "social": 4}
        }
        
        response = self.app.post('/api/match', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data["success"])
        self.assertIn("results", data)
        self.assertIn("secondary_results", data)
        
        # Verify component-wise scoring on matched curated results
        for career in data["results"]:
            self.assertIn("base_score", career)
            self.assertIn("tag_bonus", career)
            self.assertIn("driver_bonus", career)
            self.assertIn("barrier_adjustment", career)
            self.assertIn("final_score", career)
            
            calculated_sum = career["base_score"] + career["tag_bonus"] + career["driver_bonus"] + career["barrier_adjustment"]
            clamped_calculated = max(0.0, min(100.0, calculated_sum))
            self.assertAlmostEqual(career["final_score"], clamped_calculated, places=1)
            self.assertEqual(career["score"], career["final_score"])
            
        # Verify secondary matches logic
        top_curated_score = data["results"][0]["score"] if data["results"] else 0.0
        for sr in data["secondary_results"]:
            self.assertIn("soc_code", sr)
            self.assertIn("title", sr)
            self.assertIn("score", sr)
            self.assertGreater(sr["score"], top_curated_score)
            
        print("Success: Real rescaled O*NET interests successfully loaded, score components correctly isolated, and wider secondary pool matched.")

if __name__ == '__main__':
    print("Running Phase 2 app verification tests...")
    unittest.main()
