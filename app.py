import os
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from onet_loader import load_onet_data

app = Flask(__name__)
CORS(app)

# Careers Database with Milestones and Quizzes
# High Barrier indicates roles requiring expensive hardware, certifications, or long education (MLOps, Cyber, Blockchain, PM, Agile)
CAREERS_DB = [
    {
        "id": "prompt_engineer",
        "name": "Prompt Engineer",
        "riasec": {"R": 2, "I": 9, "A": 7, "S": 4, "E": 6, "C": 5},
        "tags": ["coding", "writing", "remote-work", "creative-design", "research"],
        "required_tags": ["writing"],
        "salary": 125000,
        "growth": "Explosive",
        "driver": "Passion",
        "intents": ["Full-time", "Part-time", "Hobby"],
        "high_barrier": False,
        "description": "Designs and refines AI prompts to achieve optimal responses from large language models, bridging human intent and AI execution.",
        "milestones": [
            {
                "id": 1,
                "title": "LLM Settings & System Prompts",
                "description": "Learn how settings like Temperature, Top P, and System Prompts govern model output randomness and behavioral constraints.",
                "resource_label": "Guide to LLM Parameters",
                "resource_url": "https://promptingguide.ai/introduction/settings",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary effect of increasing the Temperature parameter in an LLM?",
                            "options": ["It increases output creativity and randomness", "It speeds up inference time", "It makes the model stick strictly to facts", "It increases context window size"],
                            "answer": 0,
                            "explanation": "Temperature controls randomness: higher values (close to 1.0) increase diversity/creativity, while lower values make it deterministic."
                        },
                        {
                            "question": "Which type of prompt establishes the overall persona and rules that a model must follow throughout a conversation?",
                            "options": ["User Prompt", "Few-Shot Prompt", "System Prompt", "Chained Prompt"],
                            "answer": 2,
                            "explanation": "System prompts set the guidelines, tone, constraints, and instructions for how the model responds to any subsequent user prompts."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Few-Shot Prompting Patterns",
                "description": "Master the art of giving in-context examples to help the model learn complex formatting and reasoning behaviors without retraining.",
                "resource_label": "Few-Shot Prompting Guide",
                "resource_url": "https://promptingguide.ai/techniques/fewshot",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the key difference between Zero-Shot and Few-Shot prompting?",
                            "options": ["Few-Shot contains examples, Zero-Shot does not", "Zero-Shot requires custom python code", "Few-Shot increases model inference speed", "Few-Shot updates the model's core weights"],
                            "answer": 0,
                            "explanation": "Few-Shot prompting provides one or more examples of inputs and desired outputs inside the prompt, whereas Zero-Shot has none."
                        },
                        {
                            "question": "When structure matching (e.g. outputting valid JSON), which prompting technique is most reliable?",
                            "options": ["Asking nicely", "Few-Shot format exemplars", "Increasing Temperature", "Using shorter prompts"],
                            "answer": 1,
                            "explanation": "Providing clear structured examples (few-shot) establishes the pattern for the LLM to reproduce exactly."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Prompt Chaining & Security",
                "description": "Build pipelines that link multiple LLM calls together, and learn strategies to defend against prompt injection vulnerabilities.",
                "resource_label": "Prompt Security and Defenses",
                "resource_url": "https://promptingguide.ai/adversarial/adversarial-prompting",
                "quiz": {
                    "questions": [
                        {
                            "question": "What occurs during a Prompt Injection attack?",
                            "options": ["Untrusted user input overrides the developer instructions", "The model's API server crashes", "The model starts writing slow code", "The cost per token increases"],
                            "answer": 0,
                            "explanation": "Prompt injection happens when user inputs trick the LLM into ignoring system rules to perform unintended actions."
                        },
                        {
                            "question": "Why is 'Prompt Chaining' used in complex workflows?",
                            "options": ["It reduces API cost", "It breaks down a complex task into smaller, highly controlled sequential steps", "It bypasses prompt size limits", "It trains the model offline"],
                            "answer": 1,
                            "explanation": "Chaining breaks a big problem into steps where the output of one prompt feed as input to the next, enhancing output accuracy."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "mlops_specialist",
        "name": "MLOps Specialist",
        "riasec": {"R": 6, "I": 9, "A": 3, "S": 3, "E": 5, "C": 8},
        "tags": ["coding", "data-analysis", "remote-work", "security"],
        "required_tags": ["coding"],
        "salary": 155000,
        "growth": "High",
        "driver": "Money",
        "intents": ["Full-time"],
        "high_barrier": True,
        "description": "Deploys, monitors, and maintains machine learning models in production, ensuring system reliability and scalability.",
        "milestones": [
            {
                "id": 1,
                "title": "Docker Containerization for ML",
                "description": "Package models, code, and dependencies into reproducible Docker containers to ensure consistent execution environment.",
                "resource_label": "Docker for Machine Learning",
                "resource_url": "https://docs.docker.com/get-started/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary benefit of containerizing an ML model?",
                            "options": ["It guarantees the model runs in the exact same environment anywhere", "It automatically retrains the model", "It compresses model weights", "It writes inference code"],
                            "answer": 0,
                            "explanation": "Docker ensures that code, OS, Python libraries, and model weights are packaged identically, avoiding the 'works on my machine' issue."
                        },
                        {
                            "question": "Which Docker file instruction sets up the dependencies to run?",
                            "options": ["RUN", "EXPOSE", "COPY", "FROM"],
                            "answer": 0,
                            "explanation": "The RUN command executes setup steps in the image, such as 'pip install -r requirements.txt'."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "CI/CD Pipelines & Version Control",
                "description": "Set up automated GitHub actions to run validation tests, check for performance degradation, and build containers automatically.",
                "resource_label": "Continuous Integration in ML",
                "resource_url": "https://github.com/features/actions",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does CI/CD stand for in deployment pipelines?",
                            "options": ["Continuous Integration & Continuous Deployment", "Code Inspection & Cloud Delivery", "Calculated Inference & Coding Drive", "Critical Infrastructure & Container Deploy"],
                            "answer": 0,
                            "explanation": "CI/CD automates testing and deployment on new code updates to improve pipeline safety and speed."
                        },
                        {
                            "question": "Why is 'data versioning' crucial in ML systems compared to standard software?",
                            "options": ["Because datasets change and govern model behaviors", "Because code is not version controlled", "To minimize storage pricing", "To build fast databases"],
                            "answer": 0,
                            "explanation": "An ML model is code + data. Versioning the dataset (using tools like DVC) is necessary to reproduce training results."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Data & Concept Drift Monitoring",
                "description": "Build monitoring pipelines to log incoming data, audit accuracy trends, and flag when distribution patterns deviate from training sets.",
                "resource_label": "Introduction to Model Drift",
                "resource_url": "https://www.evidentlyai.com/ml-in-production/data-drift",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is 'Data Drift'?",
                            "options": ["The statistical distribution of model input variables changes over time", "A databases server runs out of disk space", "Network packets dropping during model inference", "The model's parameters changing during runtime"],
                            "answer": 0,
                            "explanation": "Data drift happens when real-world production inputs change statistically from the historical dataset used to train the model."
                        },
                        {
                            "question": "How do you resolve Concept Drift in production?",
                            "options": ["Retrain the model on recent, labeled data", "Decrease the temperature", "Restart the server", "Write simpler code"],
                            "answer": 0,
                            "explanation": "When the relationship between inputs and targets shift (concept drift), models must be retrained on newly captured production samples."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "ux_ui_designer",
        "name": "UX/UI Designer",
        "riasec": {"R": 2, "I": 6, "A": 10, "S": 6, "E": 5, "C": 4},
        "tags": ["creative-design", "remote-work", "client-interaction", "writing"],
        "required_tags": ["creative-design"],
        "salary": 95000,
        "growth": "High",
        "driver": "Passion",
        "intents": ["Full-time", "Part-time", "Hobby"],
        "high_barrier": False,
        "description": "Creates intuitive, user-friendly, and visually stunning digital interfaces, focusing on user journeys and interactive prototypes.",
        "milestones": [
            {
                "id": 1,
                "title": "Figma Basics & Auto Layout",
                "description": "Learn layout grids, component structures, and the power of Auto Layout to create highly responsive screen designs.",
                "resource_label": "Learn Figma Auto Layout",
                "resource_url": "https://help.figma.com/hc/en-us/articles/360040451373-Create-dynamic-layouts-with-Auto-layout",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary benefit of Figma's Auto Layout?",
                            "options": ["Designs adjust automatically when text or spacing shifts", "It converts designs directly to production HTML/CSS", "It automatically selects visual color palettes", "It edits vectors automatically"],
                            "answer": 0,
                            "explanation": "Auto layout lets you create frames that shrink or grow response to content, similar to flexbox in CSS."
                        },
                        {
                            "question": "Which constraint setting allows an item to fill the width of its parent container?",
                            "options": ["Hug contents", "Fixed width", "Fill container", "Align stretch"],
                            "answer": 2,
                            "explanation": "'Fill container' expands elements to utilize all available width/height allocated by the parent Auto Layout frame."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Wireframes & Interactive Flows",
                "description": "Build low-fidelity visual sketches, plan user navigation journeys, and link screens into clickable interactive flows.",
                "resource_label": "UI Wireframing & Flow Design",
                "resource_url": "https://www.nngroup.com/articles/wireflows/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the goal of low-fidelity wireframing?",
                            "options": ["Focus on structural layouts without getting distracted by visual polish", "Test API data transmission speeds", "Add final animations and typography styling", "Build product marketing pages"],
                            "answer": 0,
                            "explanation": "Low-fidelity wireframes focus on visual layout hierarchy, functionality, and flow, omitting colors, fonts, and assets."
                        },
                        {
                            "question": "Why do designers build interactive prototypes?",
                            "options": ["To test workflows and gather feedback before coding", "To measure backend load speeds", "To compile assets for production databases", "To automate developer commits"],
                            "answer": 0,
                            "explanation": "Clickable prototypes simulate interactions, allowing user experience teams to validate design logic and collect early feedback."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Design Systems & Visual Hierarchy",
                "description": "Create global design tokens for colors, typography, buttons, and form states to ensure consistency across product interfaces.",
                "resource_label": "Introduction to Design Systems",
                "resource_url": "https://www.uxpin.com/studio/blog/design-systems-guide/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What elements establish visual hierarchy on a screen?",
                            "options": ["Contrasting scale, color contrast, and empty spacing", "Adding more icons", "Centering all text fields", "Using the default operating system fonts"],
                            "answer": 0,
                            "explanation": "Scale, font weights, high-contrast colors, and layout whitespace guide the user's focus through the interface elements."
                        },
                        {
                            "question": "What is a major advantage of utilizing a component-driven Design System?",
                            "options": ["Changes to a master component sync globally to all instances", "It replaces the need for code implementation", "It automatically uploads to git", "It decreases the designer's pay rate"],
                            "answer": 0,
                            "explanation": "Design systems establish master components (buttons, headers), ensuring changes cascade globally, maintaining complete UI consistency."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "growth_marketer",
        "name": "Growth Marketer",
        "riasec": {"R": 1, "I": 7, "A": 6, "S": 6, "E": 9, "C": 5},
        "tags": ["data-analysis", "client-interaction", "writing", "leadership", "remote-work"],
        "required_tags": ["client-interaction"],
        "salary": 88000,
        "growth": "Steady",
        "driver": "Balance",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Drives user acquisition and retention through data-driven campaigns, creative experiments, and multi-channel marketing funnel optimization.",
        "milestones": [
            {
                "id": 1,
                "title": "Marketing Funnels & Metrics",
                "description": "Learn the AARRR (Acquisition, Activation, Retention, Referral, Revenue) framework and calculate metrics like CAC and LTV.",
                "resource_label": "Growth Funnel Framework",
                "resource_url": "https://www.growthhackers.com/aarrr",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does CAC stand for in growth marketing?",
                            "options": ["Customer Acquisition Cost", "Creative Asset Center", "Campaign Audit Code", "Channel Conversion Analytics"],
                            "answer": 0,
                            "explanation": "Customer Acquisition Cost represents total marketing and sales expenses divided by the number of new customers acquired."
                        },
                        {
                            "question": "In the AARRR framework, what metrics represent Retention?",
                            "options": ["How often customers return to use the product", "How many users click an ad", "Total monthly subscription revenue", "Customer referral rates"],
                            "answer": 0,
                            "explanation": "Retention measures active product repeat usage and metrics like churn, ensuring customers don't leave after acquiring them."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "A/B Testing Experiments",
                "description": "Design randomized campaign experiments testing headlines, copy variants, or page designs, asserting statistical significance.",
                "resource_label": "Guide to Conversion A/B Testing",
                "resource_url": "https://vwo.com/ab-testing/",
                "quiz": {
                    "questions": [
                        {
                            "question": "Why is statistical significance important in growth experiments?",
                            "options": ["It guarantees the observed metric gains aren't due to random chance", "It shortens campaign run times", "It reduces advertisement spend", "It automates media formatting"],
                            "answer": 0,
                            "explanation": "Significance calculations prove that a variant outperform a control due to user preferences, not statistical noise."
                        },
                        {
                            "question": "Which parameter should you change between Variant A and Variant B in a clean A/B test?",
                            "options": ["A single variable (e.g. only the main headline)", "All page copy, layouts, and product pricing", "The destination URL", "The target demographic audiences"],
                            "answer": 0,
                            "explanation": "A clean A/B test changes only one key variable at a time, ensuring you can isolate what caused a shift in metrics."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Attribution & Retargeting Setup",
                "description": "Understand digital tracking scripts, setting up audiences, and deploying ads across search, display, and social platforms.",
                "resource_label": "Introduction to Digital Ads Attribution",
                "resource_url": "https://support.google.com/analytics/answer/6392659",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is 'Retargeting'?",
                            "options": ["Serving advertisements specifically to users who have already visited your site", "Sending bulk newsletters", "Optimizing search engine titles", "Changing target keywords"],
                            "answer": 0,
                            "explanation": "Retargeting uses cookies or user hashes to display targeted ads to individuals who visited but didn't convert."
                        },
                        {
                            "question": "What does a first-click attribution model reward?",
                            "options": ["The channel that introduced the user to your site first", "The final conversion click", "A split distribution among all touchpoints", "Direct organic search queries"],
                            "answer": 0,
                            "explanation": "First-click attribution credits 100% of the conversion value to the initial marketing channel that brought the visitor."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "data_analyst",
        "name": "Data Analyst",
        "riasec": {"R": 2, "I": 8, "A": 3, "S": 4, "E": 5, "C": 9},
        "tags": ["data-analysis", "remote-work", "writing", "coding"],
        "required_tags": ["data-analysis"],
        "salary": 82000,
        "growth": "Steady",
        "driver": "Balance",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Transforms raw data into actionable insights, designing dashboards, performing statistical analyses, and reporting findings to stakeholders.",
        "milestones": [
            {
                "id": 1,
                "title": "SQL Query Foundations",
                "description": "Learn standard database query structures, filtering rows, grouping metrics, and joining relational tables together.",
                "resource_label": "SQL Query Course",
                "resource_url": "https://www.w3schools.com/sql/",
                "quiz": {
                    "questions": [
                        {
                            "question": "Which SQL clause is utilized to filter results based on specific row conditions?",
                            "options": ["GROUP BY", "WHERE", "ORDER BY", "SELECT"],
                            "answer": 1,
                            "explanation": "The WHERE clause acts as a logical filter, evaluating rows against conditions like 'WHERE age > 18'."
                        },
                        {
                            "question": "What type of JOIN retrieves only the rows that have matching records in both tables?",
                            "options": ["LEFT JOIN", "OUTER JOIN", "INNER JOIN", "CROSS JOIN"],
                            "answer": 2,
                            "explanation": "INNER JOIN combines rows from two tables when the join predicate matches in both, discarding unmatched records."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Interactive Dashboards & Viz",
                "description": "Master visual analytics tools like Tableau or PowerBI to configure charts, map trends, and present interactive views for stakeholders.",
                "resource_label": "Introduction to Tableau",
                "resource_url": "https://www.tableau.com/learn/training",
                "quiz": {
                    "questions": [
                        {
                            "question": "Which chart type is best suited for demonstrating trends in data over a chronological period?",
                            "options": ["Pie Chart", "Line Chart", "Scatter Plot", "Treemap"],
                            "answer": 1,
                            "explanation": "Line charts connect data points sequentially, making them excellent for evaluating trends and patterns over time."
                        },
                        {
                            "question": "What is the goal of designing an interactive dashboard?",
                            "options": ["Enable business users to query and filter metrics without writing code", "Improve model validation speeds", "Encode security encryption layers", "Build site layouts"],
                            "answer": 0,
                            "explanation": "Dashboards visualize key performance metrics with built-in controls (date sliders, category dropdowns) to empower business users."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Python Data Wrangling (Pandas)",
                "description": "Leverage Python notebooks and the Pandas library to ingest dirty CSV files, clean null data, and aggregate statistics programmatically.",
                "resource_label": "Pandas Data Wrangling Guide",
                "resource_url": "https://pandas.pydata.org/docs/user_guide/index.html",
                "quiz": {
                    "questions": [
                        {
                            "question": "In Pandas, what is a 2-dimensional labeled data structure with columns of potentially different types called?",
                            "options": ["Series", "DataFrame", "List", "Matrix"],
                            "answer": 1,
                            "explanation": "A Pandas DataFrame acts like a spreadsheet or SQL table, organizing rows and columns under column indices."
                        },
                        {
                            "question": "Which method is commonly used to drop rows containing missing or null data from a DataFrame?",
                            "options": ["dropna()", "fillna()", "drop_duplicates()", "clear()"],
                            "answer": 0,
                            "explanation": "dropna() filters out rows having null or NaN values, cleaning up datasets for reliable calculation."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "product_manager",
        "name": "Product Manager",
        "riasec": {"R": 2, "I": 6, "A": 5, "S": 8, "E": 10, "C": 6},
        "tags": ["leadership", "client-interaction", "writing", "data-analysis"],
        "required_tags": ["leadership", "client-interaction"],
        "salary": 135000,
        "growth": "High",
        "driver": "Money",
        "intents": ["Full-time"],
        "high_barrier": True,
        "description": "Defines product vision and strategy, aligns cross-functional engineering and design teams, and owns the product roadmap from inception to launch.",
        "milestones": [
            {
                "id": 1,
                "title": "Product Strategy & Requirements",
                "description": "Define product requirements documents (PRDs), structure feature lists, and translate customer feedback into actionable tasks.",
                "resource_label": "Writing a Great PRD",
                "resource_url": "https://www.productplan.com/glossary/product-requirements-document/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary role of a Product Requirements Document (PRD)?",
                            "options": ["Communicate feature scope, value, and behavior guidelines to developers and designers", "Provide code examples", "Audit database index keys", "Outline advertising budgets"],
                            "answer": 0,
                            "explanation": "A PRD aligns stakeholders on the problem, goals, scope, and specs for a feature before design and coding start."
                        },
                        {
                            "question": "Which framework structures user needs as: 'As a [user], I want [action] so that [benefit]?'",
                            "options": ["Agile Sprints", "User Story", "Kanban Board", "SWOT Analysis"],
                            "answer": 1,
                            "explanation": "User Stories focus feature development around customer value and user persona outcomes."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Prioritization Frameworks",
                "description": "Learn priority systems like RICE (Reach, Impact, Confidence, Effort) to systematically evaluate and rank backlog features.",
                "resource_label": "Guide to RICE Scoring",
                "resource_url": "https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What elements make up the RICE prioritization formula?",
                            "options": ["Reach, Impact, Confidence, Effort", "Risk, Innovation, Cost, Execution", "Resources, Identity, Cost, Evaluation", "Revenue, Interest, Customers, Engagement"],
                            "answer": 0,
                            "explanation": "RICE divides (Reach x Impact x Confidence) by Effort to output a clear, numerical value score for ranking features."
                        },
                        {
                            "question": "Why is 'Effort' in the denominator of the prioritization calculation?",
                            "options": ["Higher effort reduces the project's overall return-on-investment rating", "Higher effort increases confidence", "To reward projects that take a long time", "To double the budget requirements"],
                            "answer": 0,
                            "explanation": "Projects requiring high effort score lower in priority compared to high-impact, easy-to-build options."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Product Metrics & Analytics",
                "description": "Define North Star metrics, track retention cohorts, and run quantitative dashboards to evaluate feature performance.",
                "resource_label": "Selecting Key Product Metrics",
                "resource_url": "https://mixpanel.com/blog/product-metrics-guide/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is a 'North Star Metric'?",
                            "options": ["The key metric that best captures the core value your product delivers to customers", "Total registered user accounts", "Server uptime percentage", "Share price of the organization"],
                            "answer": 0,
                            "explanation": "The North Star Metric measures product value delivery, aligning organizational focus around long-term growth."
                        },
                        {
                            "question": "Which cohort analysis measures feature stickiness over a weekly cadence?",
                            "options": ["Retention Cohorts", "Acquisition Campaigns", "Revenue Analytics", "Server Latency Charts"],
                            "answer": 0,
                            "explanation": "Retention cohort charts trace what percentage of users return to perform actions week after week, demonstrating stickiness."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "devrel_engineer",
        "name": "DevRel Engineer",
        "riasec": {"R": 3, "I": 7, "A": 7, "S": 9, "E": 8, "C": 4},
        "tags": ["coding", "public-speaking", "client-interaction", "writing", "remote-work"],
        "required_tags": ["coding", "public-speaking"],
        "salary": 120000,
        "growth": "High",
        "driver": "Passion",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Bridges the gap between external developers and internal engineering teams by building developer relations, tutorials, speaking, and advocacy.",
        "milestones": [
            {
                "id": 1,
                "title": "SDK Writing & Documentation",
                "description": "Learn to write clear, reproducible API tutorials, code examples, and maintain developer-facing documentation.",
                "resource_label": "Writing Great Tech Docs",
                "resource_url": "https://diataxis.fr/",
                "quiz": {
                    "questions": [
                        {
                            "question": "Under the Diátaxis framework, what are the four styles of documentation?",
                            "options": ["Tutorials, How-To Guides, Reference, Explanation", "Code, Issues, PRs, Commits", "Blogs, Slides, Podcasts, Video", "API Keys, Ports, Server IP, Client ID"],
                            "answer": 0,
                            "explanation": "Diátaxis outlines Tutorials (learning-oriented), How-To Guides (task-oriented), Reference (information-oriented), and Explanation (understanding-oriented)."
                        },
                        {
                            "question": "Why are code copy-paste snippets essential in API docs?",
                            "options": ["They speed up developers' time-to-first-hello-world", "They reduce server compute bills", "They compile into python modules", "They replace source repositories"],
                            "answer": 0,
                            "explanation": "Interactive, clean snippets reduce integration friction, enabling developers to test and verify utility quickly."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Technical Presentations & Speaking",
                "description": "Structure technical presentations, create slide decks, and deliver presentations at conferences and webinars.",
                "resource_label": "Delivering Technical Talks",
                "resource_url": "https://www.oreilly.com/library/view/presentation-patterns/9780133136227/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is key when presenting code to an audience?",
                            "options": ["Show concise, syntax-highlighted snippets with enlarged fonts", "Show full raw directories of files", "Skip code entirely", "Only describe architecture verbally"],
                            "answer": 0,
                            "explanation": "Audience members can't digest long scripts on screen. Keep examples focused, high-contrast, and large."
                        },
                        {
                            "question": "How do you handle a live demo failing on stage?",
                            "options": ["Acknowledge it cleanly, switch to backup recorded video/slides, and continue", "Panic and try to compile local dependencies for 10 minutes", "Blame the conference wifi immediately and walk off", "Pretend it works anyway"],
                            "answer": 0,
                            "explanation": "Live demo failures are common. Successful speakers prepare offline screen recordings or backup slides to pivot gracefully."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Developer Feedback Loops",
                "description": "Translate external developer issues, github tickets, and community discussions into actionable roadmap feature requests.",
                "resource_label": "Advocacy Feedback Loops",
                "resource_url": "https://devrel.agency/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary role of a DevRel Engineer inside the engineering feedback loop?",
                            "options": ["Advocate for developer needs internally to improve API and DX", "Write all production unit tests", "Configure network load balancers", "Manage customer acquisition ads"],
                            "answer": 0,
                            "explanation": "DevRel aggregates community experiences, bringing crucial product friction feedback back to core product engineering teams."
                        },
                        {
                            "question": "What is DX?",
                            "options": ["Developer Experience", "Data Exchange", "Decentralized Execution", "Documentation XML"],
                            "answer": 0,
                            "explanation": "Developer Experience covers how easily and productively engineers can integrate and work with tools, APIs, and SDKs."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "sustainability_consultant",
        "name": "Sustainability Consultant",
        "riasec": {"R": 3, "I": 8, "A": 4, "S": 8, "E": 7, "C": 6},
        "tags": ["client-interaction", "research", "writing", "leadership"],
        "required_tags": ["client-interaction"],
        "salary": 92000,
        "growth": "High",
        "driver": "Balance",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Advises organizations on minimizing environmental footprint, complying with climate policies, and adopting sustainable business practices.",
        "milestones": [
            {
                "id": 1,
                "title": "Carbon Accounting Foundations",
                "description": "Learn greenhouse gas (GHG) protocols, scoping emissions (Scope 1, 2, and 3), and emissions factors.",
                "resource_label": "GHG Protocol Corporate Standard",
                "resource_url": "https://ghgprotocol.org/corporate-standard",
                "quiz": {
                    "questions": [
                        {
                            "question": "What comprises Scope 2 emissions?",
                            "options": ["Indirect emissions from purchased electricity, steam, heating, or cooling", "Direct emissions from corporate vehicles", "Supply chain vendor deliveries", "Employee business travels"],
                            "answer": 0,
                            "explanation": "Scope 2 covers indirect emissions from generation of purchased energy consumed by the reporting company."
                        },
                        {
                            "question": "Which emissions scope represents the supply chain and product lifecycle (often the hardest to measure)?",
                            "options": ["Scope 1", "Scope 2", "Scope 3", "Scope 4"],
                            "answer": 2,
                            "explanation": "Scope 3 contains all other indirect emissions throughout the corporate value chain, from raw material procurement to product end-of-life."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Sustainability Audits & ESG",
                "description": "Analyze corporate footprints, structure ESG (Environmental, Social, Governance) reports, and audit supply chain certifications.",
                "resource_label": "Understanding ESG Reporting",
                "resource_url": "https://www.sasb.org/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does ESG stand for in corporate audits?",
                            "options": ["Environmental, Social, and Governance", "Emissions, Supply-chain, and Growth", "Ethical, Sustainable, and Global", "Evaluation, Structure, and Goals"],
                            "answer": 0,
                            "explanation": "ESG defines the three central factors in measuring the sustainability and ethical impact of an investment in a company."
                        },
                        {
                            "question": "Why do sustainability consultants conduct circularity audits?",
                            "options": ["To identify waste loops and promote resource reuse and recycling", "To check server computing setups", "To verify banking balances", "To design layouts"],
                            "answer": 0,
                            "explanation": "Circularity audits ensure businesses transition from linear 'take-make-waste' lines to regenerative loops where waste is recycled."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Compliance & Corporate Strategy",
                "description": "Draft decarbonization strategies, ensure regulatory compliance with international rules, and establish carbon reduction targets.",
                "resource_label": "SBTi Target Setting Guide",
                "resource_url": "https://sciencebasedtargets.org/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What are Science-Based Targets (SBTi)?",
                            "options": ["Emissions reduction targets aligned with keeping global warming below 1.5°C", "Marketing slogans", "Database algorithms", "Financial budgets"],
                            "answer": 0,
                            "explanation": "SBTi provides targets aligned with the latest climate science for achieving Paris Agreement goals."
                        },
                        {
                            "question": "How does carbon offsetting differ from carbon reduction?",
                            "options": ["Offsetting compensates for emissions by funding external projects; reduction prevents emissions locally", "They are identical", "Offsetting is free", "Reduction involves planting trees only"],
                            "answer": 0,
                            "explanation": "Reduction minimizes output within your operations; offsetting purchases credits from external programs (e.g. reforestation) to balance footprint."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "cybersecurity_analyst",
        "name": "Cybersecurity Analyst",
        "riasec": {"R": 5, "I": 9, "A": 2, "S": 4, "E": 4, "C": 9},
        "tags": ["security", "coding", "remote-work", "data-analysis"],
        "required_tags": ["security"],
        "salary": 112000,
        "growth": "Very High",
        "driver": "Money",
        "intents": ["Full-time"],
        "high_barrier": True,
        "description": "Protects organizational network and system integrity from cyber threats, monitors security logs, audits protocols, and responds to incidents.",
        "milestones": [
            {
                "id": 1,
                "title": "Network Routing & Ports Security",
                "description": "Master TCP/IP architectures, subnetting layouts, and auditing open network ports to prevent ingress breaches.",
                "resource_label": "TCP/IP Security Fundamentals",
                "resource_url": "https://www.comptia.org/certifications/security",
                "quiz": {
                    "questions": [
                        {
                            "question": "Which protocol provides secure, encrypted remote terminal access over a network?",
                            "options": ["Telnet", "FTP", "SSH", "HTTP"],
                            "answer": 2,
                            "explanation": "SSH (Secure Shell) encrypts the terminal connection channel, replacing vulnerable unencrypted options like Telnet."
                        },
                        {
                            "question": "What standard port is utilized for secure web browsing (HTTPS)?",
                            "options": ["80", "443", "22", "8080"],
                            "answer": 1,
                            "explanation": "HTTPS runs over port 443, securing browser communication using SSL/TLS encryption."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "SIEM Auditing & Threat Analysis",
                "description": "Set up Security Information and Event Management (SIEM) consoles to capture firewall entries, analyze alerts, and map anomalies.",
                "resource_label": "SIEM Operations Guide",
                "resource_url": "https://www.splunk.com/en_us/training.html",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary function of a SIEM system?",
                            "options": ["Aggregate and analyze log inputs from across the network to detect threats", "Back up database files", "Encrypt local passwords", "Write system patches"],
                            "answer": 0,
                            "explanation": "SIEM aggregates event logs from routers, firewalls, and servers to search for real-time security alerts and indicators."
                        },
                        {
                            "question": "What represents a false positive alert in security monitoring?",
                            "options": ["Legitimate user activity flagged as a threat", "An actual breach ignored by firewalls", "A database server going offline", "A expired network certificate"],
                            "answer": 0,
                            "explanation": "False positives happen when normal operations trigger an alert, requiring analysts to tune SIEM filtering rules."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Vulnerability Patches & Auditing",
                "description": "Run vulnerability scanners, isolate configurations, and coordinate security patches to harden endpoints.",
                "resource_label": "OWASP Top 10 Security Audit",
                "resource_url": "https://owasp.org/www-project-top-ten/",
                "quiz": {
                    "questions": [
                        {
                            "question": "Which OWASP top threat category represents injection of script tags into a website database that runs in other users' browsers?",
                            "options": ["Cross-Site Scripting (XSS)", "SQL Injection", "Broken Authentication", "Security Misconfiguration"],
                            "answer": 0,
                            "explanation": "XSS vulnerabilities allow attackers to inject scripts into web pages viewed by other users, stealing session cookies or tokens."
                        },
                        {
                            "question": "What represents zero-day vulnerabilities?",
                            "options": ["Breaches actively exploited before a patch is developed", "Vulnerabilities with zero impact", "Legacy software bugs", "Expired security licenses"],
                            "answer": 0,
                            "explanation": "A zero-day is a security flaw unknown to the vendor, meaning they have 'zero days' to patch it before it can be exploited."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "blockchain_developer",
        "name": "Blockchain Developer",
        "riasec": {"R": 4, "I": 9, "A": 4, "S": 2, "E": 6, "C": 8},
        "tags": ["coding", "security", "remote-work", "data-analysis", "research"],
        "required_tags": ["coding"],
        "salary": 145000,
        "growth": "Steady",
        "driver": "Money",
        "intents": ["Full-time", "Part-time", "Hobby"],
        "high_barrier": True,
        "description": "Designs and builds decentralized protocols, smart contracts, and architecture for blockchain-based solutions and assets.",
        "milestones": [
            {
                "id": 1,
                "title": "Smart Contract Syntax (Solidity)",
                "description": "Learn variables, structure, and functions of Solidity, writing simple contracts that manage storage and states.",
                "resource_label": "CryptoZombies Solidity Course",
                "resource_url": "https://cryptozombies.io/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is a Smart Contract?",
                            "options": ["Self-executing code deployed to a decentralized blockchain ledger", "A legal PDF file", "A encrypted database query", "An advertising agreement"],
                            "answer": 0,
                            "explanation": "Smart contracts are programs stored on a blockchain that run automatically when predetermined conditions are met."
                        },
                        {
                            "question": "Which compiler target is generated when compiling Solidity files?",
                            "options": ["EVM Bytecode", "HTML/CSS", "Python scripts", "Assembly modules"],
                            "answer": 0,
                            "explanation": "Solidity compiles into Ethereum Virtual Machine (EVM) bytecode, which is executed by nodes on the network."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Local Chain Testing (Hardhat)",
                "description": "Configure local testing chains, deploy test tokens, and write scripts verifying contract outputs under network simulation.",
                "resource_label": "Hardhat Testing Framework",
                "resource_url": "https://hardhat.org/tutorial",
                "quiz": {
                    "questions": [
                        {
                            "question": "Why do blockchain developers use Hardhat?",
                            "options": ["To compile, test, and deploy smart contracts locally without paying gas fees", "To purchase crypto tokens", "To host live databases", "To write front-end styles"],
                            "answer": 0,
                            "explanation": "Hardhat provides a local Ethereum network node emulator, allowing developers to execute test scripts and debug contracts."
                        },
                        {
                            "question": "Which library is standard for connecting a Javascript UI to contract functions?",
                            "options": ["Ethers.js / Web3.js", "Django", "Chart.js", "Express"],
                            "answer": 0,
                            "explanation": "Ethers.js and Web3.js are libraries wrapping JSON-RPC nodes, allowing web clients to trigger contract inputs."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Contract Auditing & Reentrancy",
                "description": "Master blockchain security patterns, audit vulnerabilities, and secure contracts against common hacks like Reentrancy.",
                "resource_label": "Smart Contract Security Guide",
                "resource_url": "https://consensys.github.io/smart-contract-best-practices/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What characterizes a Reentrancy vulnerability in Solidity?",
                            "options": ["An external contract calls back into your contract before the balance state updates", "A database server crashing", "Exceeding the gas limit", "Entering the wrong private keys"],
                            "answer": 0,
                            "explanation": "Reentrancy occurs when a contract sends funds to an untrusted contract before updating its internal ledger, allowing the recipient to withdraw repeatedly."
                        },
                        {
                            "question": "What keyword is utilized in Solidity to declare immutable global constants?",
                            "options": ["constant / immutable", "let", "var", "final"],
                            "answer": 0,
                            "explanation": "Declaring state variables as 'constant' or 'immutable' saves significant gas and prevents variable modification after deployment."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "ai_ethicist",
        "name": "AI Ethicist",
        "riasec": {"R": 1, "I": 9, "A": 7, "S": 8, "E": 5, "C": 6},
        "tags": ["research", "writing", "public-speaking", "remote-work", "client-interaction"],
        "required_tags": ["research", "writing"],
        "salary": 105000,
        "growth": "Emerging",
        "driver": "Passion",
        "intents": ["Full-time", "Part-time", "Hobby"],
        "high_barrier": False,
        "description": "Evaluates societal, moral, and regulatory impacts of AI systems, establishing safety frameworks and ethical guidelines for research and deploy.",
        "milestones": [
            {
                "id": 1,
                "title": "Algorithmic Bias & Fair Metrics",
                "description": "Learn math metrics for fairness (demographic parity, equalized odds) and audit datasets for historical bias.",
                "resource_label": "Google's Guide to Machine Learning Fairness",
                "resource_url": "https://developers.google.com/machine-learning/fairness-overview",
                "quiz": {
                    "questions": [
                        {
                            "question": "What represents algorithmic bias?",
                            "options": ["Systemic, unfair errors in model predictions favoring certain groups over others", "A compilation crash", "High server network latency", "Small training data file sizes"],
                            "answer": 0,
                            "explanation": "Algorithmic bias occurs when trained models reproduce or amplify prejudices present in the training datasets."
                        },
                        {
                            "question": "What is 'Demographic Parity' in fairness audits?",
                            "options": ["Ensuring positive predictions occur in equal proportions across all subgroups", "Reducing model parameters", "Balancing server loads", "Writing clean comments"],
                            "answer": 0,
                            "explanation": "Demographic parity evaluates if the likelihood of a positive outcome (e.g. loan approval) is identical regardless of protected traits (e.g. gender)."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Explainable AI (XAI) & Metrics",
                "description": "Understand model interpretability methods like SHAP and LIME to explain complex black-box model decisions.",
                "resource_label": "Interpretability & Explainable AI",
                "resource_url": "https://christophm.github.io/interpretable-ml-book/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is explainable AI (XAI)?",
                            "options": ["Techniques ensuring human experts can trace and comprehend how models reach decisions", "Generating automated comments", "Using simpler models", "Running database logs"],
                            "answer": 0,
                            "explanation": "XAI provides frameworks to interpret complex predictions (e.g. deep neural networks) to ensure accountability and safety."
                        },
                        {
                            "question": "How do SHAP values help interpret model outputs?",
                            "options": ["They calculate each feature's contribution to the final prediction score", "They speed up server training", "They compress file weights", "They select learning rates"],
                            "answer": 0,
                            "explanation": "SHAP (SHapley Additive exPlanations) utilizes game theory to attribute feature contributions to individual predictions."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "AI Safety, Governance, & Policy",
                "description": "Analyze regulatory guidelines (like the EU AI Act) and establish safety rules for generative models.",
                "resource_label": "Understanding the EU AI Act",
                "resource_url": "https://artificialintelligenceact.eu/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What compliance risk category does the EU AI Act assign to biometric categorization systems?",
                            "options": ["High Risk / Prohibited", "Low Risk", "Minimal Risk", "Exempt"],
                            "answer": 0,
                            "explanation": "Real-time biometric classification and social scoring are categorized as high-risk or prohibited under the act."
                        },
                        {
                            "question": "What represents red-teaming in generative AI safety?",
                            "options": ["Actively probing models to trigger rule violations, leakage, or harmful responses", "Writing unit tests", "Hosting server nodes", "Creating sales decks"],
                            "answer": 0,
                            "explanation": "Red-teaming is adversarial safety testing where team members try to break LLM safeguards before deployment."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "customer_success_manager",
        "name": "Customer Success Manager",
        "riasec": {"R": 1, "I": 4, "A": 4, "S": 9, "E": 8, "C": 6},
        "tags": ["client-interaction", "remote-work", "writing", "leadership"],
        "required_tags": ["client-interaction"],
        "salary": 78000,
        "growth": "Steady",
        "driver": "Balance",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Partners with SaaS customers to guide onboarding, maximize platform value, prevent churn, and drive long-term business retention.",
        "milestones": [
            {
                "id": 1,
                "title": "Customer Onboarding Journeys",
                "description": "Map customer milestones from contract signing to first-value activation, setting up metrics dashboards.",
                "resource_label": "SaaS Customer Onboarding Best Practices",
                "resource_url": "https://www.gainsight.com/customer-success-university/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What represents 'Time-to-Value' (TTV) in customer onboarding?",
                            "options": ["The time it takes for a customer to realize their first business benefit from the software", "Total subscription billing time", "The duration of the sales negotiations", "The server installation phase"],
                            "answer": 0,
                            "explanation": "TTV is a critical metric: shorter TTV leads to higher customer activation and reduced early retention churn."
                        },
                        {
                            "question": "Which dashboard visualizes customer health scores?",
                            "options": ["Customer Success CRM (e.g. Gainsight)", "SQL Database Schema", "Version Control Console", "Ad Campaign Manager"],
                            "answer": 0,
                            "explanation": "CSM platforms aggregate customer activity, support tickets, and billing details to index overall health score."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Churn Prevention & Metrics",
                "description": "Analyze health metrics (Net Promoter Score, product usage depth) and proactively intervene on low-usage accounts.",
                "resource_label": "Guide to SaaS Churn Metric Formulas",
                "resource_url": "https://www.klipfolio.com/resources/kpi-examples/customer-success/churn-rate",
                "quiz": {
                    "questions": [
                        {
                            "question": "How is Churn Rate mathematically calculated?",
                            "options": ["Customers lost during a period divided by active customers at start of period", "Revenue gained divided by CAC", "Active users divided by total page views", "Acquisitions divided by cancellations"],
                            "answer": 0,
                            "explanation": "Churn rate is calculated as the ratio of cancellations over a timeframe relative to customer count at the start."
                        },
                        {
                            "question": "What represents Net Revenue Retention (NRR)?",
                            "options": ["Revenue retention including upgrades and expansions, excluding churn", "Total gross earnings before taxes", "Total subscription marketing costs", "Average billing values"],
                            "answer": 0,
                            "explanation": "NRR measures recurring revenue from existing customers over time, factoring in churn, contraction, and expansion."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Upsells, QBRs & Expansions",
                "description": "Host Quarterly Business Reviews (QBRs) with clients, demonstrating product value and structuring expansion agreements.",
                "resource_label": "Running Impactful QBRs",
                "resource_url": "https://www.clientsuccess.com/blog/how-to-run-a-qbr/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary objective of a Quarterly Business Review (QBR)?",
                            "options": ["Align on client achievements, demonstrate ROI, and verify long-term partnership goals", "Renegotiate contract terms", "Troubleshoot software bugs", "Draft advertising copy"],
                            "answer": 0,
                            "explanation": "QBRs prove the product's business value, align goals, and pave the way for customer contract renewal and expansion."
                        },
                        {
                            "question": "How does Upselling differ from Cross-selling?",
                            "options": ["Upselling sells higher tiers; Cross-selling sells complementary products", "They are identical", "Upselling is illegal", "Cross-selling is free"],
                            "answer": 0,
                            "explanation": "Upselling moves clients to a premium version or seat level; cross-selling introduces a completely separate module or service."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "digital_content_strategist",
        "name": "Digital Content Strategist",
        "riasec": {"R": 1, "I": 5, "A": 9, "S": 6, "E": 7, "C": 4},
        "tags": ["creative-design", "writing", "remote-work", "client-interaction"],
        "required_tags": ["writing", "creative-design"],
        "salary": 85000,
        "growth": "High",
        "driver": "Passion",
        "intents": ["Full-time", "Part-time", "Hobby"],
        "high_barrier": False,
        "description": "Develops and executes multi-channel content strategies, overseeing creation of visual and written media assets to drive brand audience engagement.",
        "milestones": [
            {
                "id": 1,
                "title": "SEO Foundations & Content Briefs",
                "description": "Master keyword research tools, plan semantic architectures, and outline standard content briefs for creation.",
                "resource_label": "SEO Keyword Strategy Guide",
                "resource_url": "https://moz.com/beginners-guide-to-seo",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does a search engine optimization (SEO) content brief specify?",
                            "options": ["Keyword targets, user intent, content outline, and visual suggestions", "Full HTML templates", "Server database ports", "Contract billing margins"],
                            "answer": 0,
                            "explanation": "Content briefs align writers and creators on target terms, headings structure, and user search intent before writing begins."
                        },
                        {
                            "question": "Which metric evaluates search query competitiveness?",
                            "options": ["Keyword Difficulty", "Domain Authority", "Click-through rate", "Search impressions"],
                            "answer": 0,
                            "explanation": "Keyword Difficulty predicts how hard it is to rank on the first page of search results for a specific phrase."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Content Calendars & Lifecycle",
                "description": "Configure multi-channel editorial calendars, mapping content assets to the marketing awareness funnel.",
                "resource_label": "Building Content Calendars",
                "resource_url": "https://hubspot.com/marketing/editorial-calendar-template",
                "quiz": {
                    "questions": [
                        {
                            "question": "Why do strategists build Content Calendars?",
                            "options": ["Coordinate publication schedules, team workflows, and brand messaging across channels", "Test local network connections", "Draft code functions", "Calculate advertising budgets"],
                            "answer": 0,
                            "explanation": "Calendars track channels, dates, and ownership, ensuring consistent publication and aligning marketing campaigns."
                        },
                        {
                            "question": "What content format is best for Top-of-Funnel (TOFU) awareness?",
                            "options": ["SEO blog posts, social summaries, and educational videos", "Detailed pricing spreadsheets", "Product demo trials", "Contract terms details"],
                            "answer": 0,
                            "explanation": "TOFU content targets broad education and search discovery, introducing prospects to the brand ecosystem."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Asset Distribution & Analytics",
                "description": "Set up tracking tags, analyze post-engagement patterns, and refine keyword campaigns based on conversion rates.",
                "resource_label": "Google Analytics Content Tracking",
                "resource_url": "https://analytics.google.com/analytics/academy/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What parameter is added to URLs to track specific campaign channels?",
                            "options": ["UTM parameters", "CSS styles", "API keys", "Session hashes"],
                            "answer": 0,
                            "explanation": "UTM (Urchin Tracking Module) codes track traffic source, medium, and campaign name in Google Analytics."
                        },
                        {
                            "question": "What does a high bounce rate on an informational page suggest?",
                            "options": ["The content didn't match the search intent or user expectation", "The server has network errors", "The page is too fast", "The page lacks image assets"],
                            "answer": 0,
                            "explanation": "Bounce rates suggest users left the page without interacting, indicating irrelevant content or bad experience."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "talent_acquisition_partner",
        "name": "Talent Acquisition Partner",
        "riasec": {"R": 1, "I": 4, "A": 4, "S": 9, "E": 8, "C": 6},
        "tags": ["client-interaction", "leadership", "writing", "remote-work"],
        "required_tags": ["client-interaction"],
        "salary": 80000,
        "growth": "Steady",
        "driver": "Balance",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Identifies, recruits, and builds relationships with top professional talent, designing candidate pipelines and negotiating career offers.",
        "milestones": [
            {
                "id": 1,
                "title": "Candidate Sourcing & Queries",
                "description": "Master advanced search queries (Boolean strings) on platforms like LinkedIn and construct email outreach pipelines.",
                "resource_label": "Boolean Sourcing Guide",
                "resource_url": "https://www.socialtalents.com/",
                "quiz": {
                    "questions": [
                        {
                            "question": "Which Boolean search string retrieves resumes having 'Python' and either 'Flask' or 'Django'?",
                            "options": ["Python AND (Flask OR Django)", "Python OR (Flask AND Django)", "Python AND Flask Django", "Python NOT Flask django"],
                            "answer": 0,
                            "explanation": "AND requires both criteria, while parentheses group the OR statement, returning matches with either framework."
                        },
                        {
                            "question": "What is the goal of a personalized candidate outreach template?",
                            "options": ["Increase outreach reply rates and build early engagement", "Automate code commits", "Filter salaries", "Verify background documents"],
                            "answer": 0,
                            "explanation": "Personalized messages demonstrating knowledge of the candidate's achievements dramatically increase response rates."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Behavioral Interview Structures",
                "description": "Design structured interview rubrics (STAR method) to evaluate candidate competencies objectively.",
                "resource_label": "STAR Interview Method Guide",
                "resource_url": "https://www.shrm.org/resourcesandtools/tools-and-samples/pages/behavioral-interviewing.aspx",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does the acronym STAR stand for in interview structures?",
                            "options": ["Situation, Task, Action, Result", "Salary, Target, Agreement, Review", "Sourcing, Testing, Allocation, Recruiter", "System, Time, Access, Role"],
                            "answer": 0,
                            "explanation": "STAR guides candidates to describe the Situation, Task, Action taken, and the quantitative Result achieved."
                        },
                        {
                            "question": "Why are structured rubrics preferred over unstructured interviews?",
                            "options": ["They minimize hiring bias and improve score reliability", "They shorten calls", "They allow negotiating salaries", "They select candidates automatically"],
                            "answer": 0,
                            "explanation": "Applying consistent questions and grading matrices ensures candidates are evaluated fairly on merit, minimizing bias."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Offer Negotiation & Onboarding",
                "description": "Structure compensation structures, present offers, handle candidate objections, and coordinate compliance records.",
                "resource_label": "Negotiating Talent Compensation",
                "resource_url": "https://www.recruiter.com/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What constitutes a total compensation package?",
                            "options": ["Base salary plus stock options, healthcare benefits, and performance bonuses", "Only the base salary rate", "Hourly billing rates", "An advertising budget"],
                            "answer": 0,
                            "explanation": "Total compensation encompasses base pay, equity grants, health insurance, matching 401(k), and bonuses."
                        },
                        {
                            "question": "How do partners resolve salary expectation gap objections?",
                            "options": ["Present total value details, add sign-on bonuses, or negotiate remote-work flexibility", "Immediately decline candidates", "Offer cash under the table", "Fake local market surveys"],
                            "answer": 0,
                            "explanation": "Recruiters align expectation gaps by highlighting total rewards value, performance adjustments, or remote flexibilities."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "agile_scrum_master",
        "name": "Agile Scrum Master",
        "riasec": {"R": 2, "I": 5, "A": 3, "S": 9, "E": 7, "C": 8},
        "tags": ["leadership", "client-interaction", "remote-work", "data-analysis"],
        "required_tags": ["leadership"],
        "salary": 105000,
        "growth": "High",
        "driver": "Balance",
        "intents": ["Full-time"],
        "high_barrier": True,
        "description": "Facilitates agile team sprints, coaching cross-functional software and ops teams on scrum methodology and removing delivery blockers.",
        "milestones": [
            {
                "id": 1,
                "title": "Scrum Framework & Roles",
                "description": "Learn the pillars of Scrum, sprint structures, and differences between Scrum Master, Product Owner, and Development Team.",
                "resource_label": "The Official Scrum Guide",
                "resource_url": "https://scrumguides.org/scrum-guide.html",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary role of the Product Owner in Scrum?",
                            "options": ["Define feature priorities and maximize product backlog value", "Manage developer daily tasks", "Facilitate daily scrums", "Write deployment containers"],
                            "answer": 0,
                            "explanation": "Product Owners own the backlog, defining what features to build and ordering priorities to optimize product value."
                        },
                        {
                            "question": "Which Scrum event is designed to inspect progress and adjust priorities on a daily cadence?",
                            "options": ["Daily Scrum", "Sprint Planning", "Sprint Retrospective", "Sprint Review"],
                            "answer": 0,
                            "explanation": "The Daily Scrum is a short 15-minute sync for team members to inspect progress towards the sprint goal."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Sprint Management (Jira)",
                "description": "Set up sprint boards, track tasks, and analyze velocity metrics (Burndown charts, Cumulative flows).",
                "resource_label": "Atlassian Agile Jira Tutorial",
                "resource_url": "https://www.atlassian.com/agile/tutorials",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does a Burndown chart demonstrate?",
                            "options": ["The remaining work against the planned timeline in a sprint", "Total code lines updated", "Server processing speeds", "Budget spending metrics"],
                            "answer": 0,
                            "explanation": "Burndown charts track completed tasks and story points against chronological progress, indicating if a sprint will complete on target."
                        },
                        {
                            "question": "What is team 'Velocity' in Scrum?",
                            "options": ["The average number of story points completed by a team per sprint", "The network speed of server nodes", "The rate of code commits", "The design prototype creation time"],
                            "answer": 0,
                            "explanation": "Velocity helps predict how much work the team can reliably commit to in future planning sprints."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Retrospectives & Agile Coaching",
                "description": "Facilitate retrospectives (Sprint reflection), handle team conflicts, and coach managers on agile values.",
                "resource_label": "Running Effective Retrospectives",
                "resource_url": "https://www.easyretro.io/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the goal of a Sprint Retrospective?",
                            "options": ["Reflect on the past sprint to identify process improvements for the next one", "Demo features to users", "Estimate backlog story points", "Audit database schemas"],
                            "answer": 0,
                            "explanation": "Retrospectives focus on team processes, collaboration, and tools, planning action items to improve efficiency."
                        },
                        {
                            "question": "How does a Scrum Master handle external team dependencies and operational blockers?",
                            "options": ["Actively coordinates with other teams to unblock the developers", "Asks developers to resolve it during off-hours", "Logs a ticket and waits indefinitely", "Changes the project timeline"],
                            "answer": 0,
                            "explanation": "Scrum Masters act as servant leaders, actively managing dependencies and removing roadblocks to keep developers focused."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "fintech_financial_planner",
        "name": "Fintech Financial Planner",
        "riasec": {"R": 2, "I": 7, "A": 2, "S": 6, "E": 8, "C": 9},
        "tags": ["data-analysis", "client-interaction", "remote-work", "security"],
        "required_tags": ["data-analysis", "client-interaction"],
        "salary": 115000,
        "growth": "High",
        "driver": "Money",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Advises individuals and organizations on financial strategy, utilizing modern algorithmic planning platforms and asset allocations.",
        "milestones": [
            {
                "id": 1,
                "title": "Asset Classes & Portfolio Math",
                "description": "Understand modern portfolio theory, risk metrics (standard deviation, beta), and tax-advantaged structures.",
                "resource_label": "Modern Portfolio Theory Basics",
                "resource_url": "https://www.investopedia.com/terms/m/modernportfoliotheory.asp",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the primary objective of asset diversification?",
                            "options": ["Minimize portfolio risk by combining uncorrelated assets", "Maximize short-term stock trading profits", "Reduce taxation on deposits", "Speed up transaction execution"],
                            "answer": 0,
                            "explanation": "Diversification reduces volatility and specific asset risk, balancing returns across different sectors or classes."
                        },
                        {
                            "question": "What does a Beta of 1.2 suggest about a stock relative to the market?",
                            "options": ["It is 20% more volatile than the overall market", "It is 20% less volatile", "It pays a 12% annual dividend", "It is highly secure and index-pegged"],
                            "answer": 0,
                            "explanation": "Beta measures systematic volatility: a value of 1.0 matches the market; values > 1.0 indicate higher volatility."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Algorithmic Wealth Modeling",
                "description": "Leverage Fintech software platforms (e.g. eMoney, RightCapital) to calculate cashflows and run Monte Carlo simulations.",
                "resource_label": "Fintech Planning Platforms Guide",
                "resource_url": "https://www.kitces.com/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is a Monte Carlo simulation in financial forecasting?",
                            "options": ["Running thousands of randomized market return sequences to calculate probability of success", "A casino strategy algorithm", "A tax calculation method", "A marketing funnel analysis"],
                            "answer": 0,
                            "explanation": "Monte Carlo models project likelihood of retirement funding success under diverse market sequences, avoiding static averages."
                        },
                        {
                            "question": "What target metric does a Monte Carlo report display?",
                            "options": ["Probability of not running out of funds (e.g. 85% success rate)", "Maximum stock price targets", "Credit card transaction speeds", "Advertising CPC rates"],
                            "answer": 0,
                            "explanation": "It reports the percentage of random trials where the client does not deplete their capital before lifespan limits."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Tax Optimization & Estates",
                "description": "Structure tax-efficient withdrawal sequences, analyze trust accounts, and advise on estate legacy structures.",
                "resource_label": "Tax-Efficient Withdrawal Sequences",
                "resource_url": "https://www.irs.gov/retirement-plans",
                "quiz": {
                    "questions": [
                        {
                            "question": "Which account withdraw sequence is generally most tax-efficient?",
                            "options": ["Taxable accounts first, then tax-deferred (Traditional), then tax-free (Roth)", "Roth accounts first, then Traditional, then taxable", "Traditional first, then taxable, then Roth", "Random split payouts"],
                            "answer": 0,
                            "explanation": "Taxable accounts grow slower due to annual tax drag, so spending them first lets tax-advantaged accounts compound longer."
                        },
                        {
                            "question": "What represents a Traditional vs Roth tax structures?",
                            "options": ["Traditional offers upfront tax deductions; Roth offers tax-free withdrawals in retirement", "Traditional is free; Roth charges fees", "Roth is for corporate accounts only", "Traditional is peg-linked to stocks"],
                            "answer": 0,
                            "explanation": "Traditional plans use pre-tax funds and tax payouts later; Roth plans use post-tax funds, allowing tax-free distribution."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "healthcare_informatics_specialist",
        "name": "Healthcare Informatics Specialist",
        "riasec": {"R": 4, "I": 8, "A": 2, "S": 6, "E": 4, "C": 8},
        "tags": ["data-analysis", "remote-work", "writing", "security"],
        "required_tags": ["data-analysis"],
        "salary": 98000,
        "growth": "Very High",
        "driver": "Balance",
        "intents": ["Full-time"],
        "high_barrier": False,
        "description": "Bridges healthcare workflows and database systems, auditing health records flow and optimizing clinical software tools.",
        "milestones": [
            {
                "id": 1,
                "title": "EHR Architectures & Standards",
                "description": "Master medical records structures (HL7, FHIR protocols) to format patient data exchanges.",
                "resource_label": "Introduction to FHIR Protocol",
                "resource_url": "https://hl7.org/fhir/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the FHIR standard in healthcare databases?",
                            "options": ["Fast Healthcare Interoperability Resources", "Federal Health Insurance Records", "File Handling and Ingestion Rules", "Free Health Integration Repository"],
                            "answer": 0,
                            "explanation": "FHIR is a standard describing data formats and resources for exchanging electronic health records via REST APIs."
                        },
                        {
                            "question": "What is HL7 primarily utilized for?",
                            "options": ["Structuring clinical message exchanges between disparate medical systems", "Analyzing MRI graphics", "Filing tax compliance", "Running ad funnels"],
                            "answer": 0,
                            "explanation": "HL7 (Health Level Seven) provides standards for transfer of clinical and administrative data between software applications."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "HIPAA Audits & Record Flows",
                "description": "Analyze database logs, ensure HIPAA privacy and security compliance, and secure data pipelines.",
                "resource_label": "HIPAA Privacy and Security Rules",
                "resource_url": "https://www.hhs.gov/hipaa/index.html",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does HIPAA protect in healthcare systems?",
                            "options": ["Protected Health Information (PHI) of patients", "Corporate banking values", "Doctor salary rates", "Ad campaign metrics"],
                            "answer": 0,
                            "explanation": "HIPAA regulations establish national standards to protect sensitive patient health information from disclosure without consent."
                        },
                        {
                            "question": "What is a Business Associate Agreement (BAA)?",
                            "options": ["A legal contract governing third-party vendors handling PHI", "An advertising contract", "A database index design", "A code license key"],
                            "answer": 0,
                            "explanation": "BAAs bind subcontractors to HIPAA security standards, ensuring client protection across integrated software tools."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Clinical Analytics & Quality Metrics",
                "description": "Audit medical charts to report clinical quality metrics (HEDIS, MIPS) to regulatory bodies.",
                "resource_label": "Understanding HEDIS Metrics",
                "resource_url": "https://www.ncqa.org/hedis/",
                "quiz": {
                    "questions": [
                        {
                            "question": "What does HEDIS measure in clinical databases?",
                            "options": ["Performance metrics of care quality and health plan services", "Database query execution times", "Staffing hours", "Marketing click-through rates"],
                            "answer": 0,
                            "explanation": "HEDIS is a widely used performance tool measuring effectiveness, accessibility, and quality of clinical treatments."
                        },
                        {
                            "question": "Why do informatics specialists structure clean schemas for analytics?",
                            "options": ["To identify care improvement gaps and submit accurate reports to regulators", "To speed up code compilation", "To reduce web app visual size", "To design custom fonts"],
                            "answer": 0,
                            "explanation": "Structured medical registries allow analytics dashboards to pull metrics reliably, improving patient tracking and compliance."
                        }
                    ]
                }
            }
        ]
    },
    {
        "id": "ecommerce_brand_manager",
        "name": "E-commerce Brand Manager",
        "riasec": {"R": 2, "I": 6, "A": 6, "S": 5, "E": 9, "C": 7},
        "tags": ["leadership", "data-analysis", "creative-design", "remote-work", "client-interaction"],
        "required_tags": ["leadership"],
        "salary": 90000,
        "growth": "Steady",
        "driver": "Money",
        "intents": ["Full-time", "Part-time"],
        "high_barrier": False,
        "description": "Manages digital retail storefronts, overseeing inventory logistics, brand listing visuals, marketing campaigns, and funnel analytics.",
        "milestones": [
            {
                "id": 1,
                "title": "Shopify Store & SEO Listings",
                "description": "Configure digital retail storefronts, design listings, and optimize metadata titles for organic search engines.",
                "resource_label": "Shopify Academy Store Setup",
                "resource_url": "https://www.shopify.com/learn",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the goal of product page search engine optimization (SEO)?",
                            "options": ["Increase page visibility and organic traffic to product listings", "Compress image assets", "Validate database schemas", "Speed up billing scripts"],
                            "answer": 0,
                            "explanation": "Optimizing titles, descriptions, and tags drives search engine visibility, drawing high-intent shoppers."
                        },
                        {
                            "question": "What role does a Product Information Management (PIM) system play?",
                            "options": ["Centralizes product data, listings, and assets across storefronts", "Calculates payroll salaries", "Hosts the storefront server", "Decrypts password logs"],
                            "answer": 0,
                            "explanation": "PIM systems serve as a single source of truth for product descriptions, pricing, and media, distributing to Amazon, Shopify, etc."
                        }
                    ]
                }
            },
            {
                "id": 2,
                "title": "Inventory Planning & Supply Chain",
                "description": "Calculate stock parameters, forecast turnover cycles, and manage fulfillment relationships (3PL, dropshipping).",
                "resource_label": "Inventory Operations Basics",
                "resource_url": "https://www.investopedia.com/terms/i/inventory-turnover.asp",
                "quiz": {
                    "questions": [
                        {
                            "question": "How is Inventory Turnover calculated?",
                            "options": ["Cost of Goods Sold (COGS) divided by average inventory value", "Total revenues divided by unit count", "Acquisition cost divided by net profit", "Fulfillment time in days"],
                            "answer": 0,
                            "explanation": "Turnover measures how rapidly inventory is sold and replaced: higher ratios indicate strong efficiency."
                        },
                        {
                            "question": "What is a 3PL in digital retail logistics?",
                            "options": ["Third-Party Logistics provider managing warehousing, picking, and shipping", "A database protocol", "A advertising channel", "A pricing metric"],
                            "answer": 0,
                            "explanation": "3PLs warehouse inventory and package/ship orders directly on integration with the online store checkout."
                        }
                    ]
                }
            },
            {
                "id": 3,
                "title": "Ad ROI & Funnel Analytics",
                "description": "Analyze ROAS (Return on Ad Spend), optimize conversion rates, and map average order values (AOV).",
                "resource_label": "Calculating E-commerce ROAS",
                "resource_url": "https://www.shopify.com/blog/roas-formula",
                "quiz": {
                    "questions": [
                        {
                            "question": "What is the formula for Return on Ad Spend (ROAS)?",
                            "options": ["Gross revenue generated from ads divided by total ad spend", "Net earnings divided by CAC", "Page views divided by ad budget", "Conversion rate divided by order value"],
                            "answer": 0,
                            "explanation": "ROAS measures ad effectiveness: if $100 in ads earns $400 in revenue, the ROAS is 4.0x or 400%."
                        },
                        {
                            "question": "What representing Average Order Value (AOV)?",
                            "options": ["Total sales revenue divided by number of orders", "The average price of single assets", "Average customer shipping cost", "Monthly recurring revenue"],
                            "answer": 0,
                            "explanation": "AOV represents the average amount spent per checkout order, which brands improve via upselling and bundling."
                        }
                    ]
                }
            }
        ]
    }
]

CURATED_SOC_MAPPING = {
    "prompt_engineer": "15-2051.00",
    "mlops_specialist": "15-1299.08",
    "ux_ui_designer": "15-1255.00",
    "growth_marketer": "13-1161.01",
    "data_analyst": "15-2051.01",
    "product_manager": "15-1299.09",
    "devrel_engineer": "15-1252.00",
    "sustainability_consultant": "13-1199.05",
    "cybersecurity_analyst": "15-1212.00",
    "blockchain_developer": "15-1299.07",
    "ai_ethicist": "15-1221.00",
    "customer_success_manager": "41-3091.00",
    "digital_content_strategist": "27-3043.00",
    "talent_acquisition_partner": "13-1071.00",
    "agile_scrum_master": "13-1082.00",
    "fintech_financial_planner": "13-2052.00",
    "healthcare_informatics_specialist": "15-1211.01",
    "ecommerce_brand_manager": "11-2021.00",
}

# Load O*NET database
try:
    ONET_DB = load_onet_data()
except Exception as e:
    print(f"Warning: Failed to load O*NET data at startup: {e}")
    ONET_DB = {}

# Override hardcoded RIASEC scores with real O*NET data
for career in CAREERS_DB:
    soc_code = CURATED_SOC_MAPPING.get(career["id"])
    if soc_code and soc_code in ONET_DB:
        # Keep original RIASEC for testing/validation
        career["original_riasec"] = career["riasec"].copy()
        career["riasec"] = ONET_DB[soc_code]["riasec"]
        career["onet_soc_code"] = soc_code
        print(f"Overrode {career['name']} with O*NET data {soc_code}: {career['riasec']}")
    else:
        print(f"Warning: Could not override {career['name']}, SOC: {soc_code} not found in O*NET DB")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['POST'])
def match():
    data = request.get_json() or {}
    
    # Extract values
    user_riasec = data.get('riasec', {})
    likes = data.get('likes', [])
    dislikes = data.get('dislikes', [])
    intent = data.get('intent', 'Full-time')
    current_role = data.get('current_role', 'Student')
    driver = data.get('driver', 'Passion')
    financial_flexibility = data.get('financial_flexibility', 'Medium') # 'Low', 'Medium', 'High'
    
    # Parse RIASEC values to floats/ints (range 0 to 10)
    dimensions = ["R", "I", "A", "S", "E", "C"]
    parsed_user_riasec = {}
    for dim in dimensions:
        val = user_riasec.get(dim)
        if val is None or val == "" or val == "null" or val == "None":
            parsed_user_riasec[dim] = None
        else:
            parsed_user_riasec[dim] = float(val)
        
    matched_careers = []
    
    for career in CAREERS_DB:
        # 1. HARD EXCLUSION: If any of career's required_tags are in user's dislikes
        exclude = False
        for req_tag in career["required_tags"]:
            if req_tag in dislikes:
                exclude = True
                break
        
        # 2. HARD EXCLUSION: Intent mismatch
        if intent not in career["intents"]:
            exclude = True
            
        if exclude:
            continue
            
        # 3. RIASEC SCORE (Manhattan Distance normalized to 100%)
        total_dist = 0
        career_riasec = career["riasec"]
        valid_dims = 0
        for dim in dimensions:
            u_val = parsed_user_riasec.get(dim)
            if u_val is not None:
                c_val = career_riasec.get(dim, 5.0)
                total_dist += abs(c_val - u_val)
                valid_dims += 1
            
        if valid_dims > 0:
            riasec_score = 1.0 - (total_dist / (valid_dims * 10.0))
        else:
            riasec_score = 1.0
        base_match_score = riasec_score * 100.0
        
        # 4. TAG BONUSES (likes)
        bonus_tags = 0
        matching_tags = []
        for tag in likes:
            if tag in career["tags"]:
                bonus_tags += 4.0
                matching_tags.append(tag)
                
        # 5. PRIMARY DRIVER MATCH
        driver_bonus = 0.0
        if driver == career["driver"]:
            driver_bonus = 10.0
            
        # 6. FINANCIAL FLEXIBILITY AND BARRIER CONSTRAINT ADJUSTMENTS
        barrier_adjustment = 0.0
        if financial_flexibility == 'Low' and career.get("high_barrier", False):
            barrier_adjustment = -15.0 # -15% penalty
        elif financial_flexibility == 'High' and career.get("high_barrier", False):
            barrier_adjustment = 5.0 # +5% bonus
            
        # Boost low-barrier options if low flexibility is chosen
        low_flex_boost = 0.0
        if financial_flexibility == 'Low' and not career.get("high_barrier", False) and intent in ['Part-time', 'Hobby']:
            low_flex_boost = 10.0 # +10% boost
            
        # Total score calculation
        total_score = base_match_score + bonus_tags + driver_bonus + barrier_adjustment + low_flex_boost
        # Clamp between 0 and 100
        total_score = max(0.0, min(100.0, total_score))
        
        # Generate Dynamic explanation
        active_traits = {k: v for k, v in parsed_user_riasec.items() if v is not None}
        if active_traits:
            sorted_user_traits = sorted(active_traits.items(), key=lambda x: x[1], reverse=True)
            dominant_trait_key = sorted_user_traits[0][0]
        else:
            dominant_trait_key = "A"
        trait_names = {
            "R": "Realistic (Doer)",
            "I": "Investigative (Thinker)",
            "A": "Artistic (Creator)",
            "S": "Social (Helper)",
            "E": "Enterprising (Persuader)",
            "C": "Conventional (Organizer)"
        }
        dominant_trait_name = trait_names.get(dominant_trait_key, "creative")
        
        explanation_parts = []
        explanation_parts.append(
            f"Your high affinity for {dominant_trait_name} activities aligns well with the "
            f"core workflows of a {career['name']}."
        )
        
        if matching_tags:
            formatted_tags = [t.replace('-', ' ') for t in matching_tags[:2]]
            explanation_parts.append(
                f"Your preferences for {', '.join(formatted_tags)} match this role's environment."
            )
            
        if driver == career["driver"]:
            explanation_parts.append(
                f"It also perfectly caters to your primary motivator: {driver}."
            )
            
        if financial_flexibility == 'Low' and career.get("high_barrier", False):
            explanation_parts.append(
                "Note: Highly technical barriers require investment, which may conflict with your low financial flexibility."
            )
        elif financial_flexibility == 'Low' and not career.get("high_barrier", False):
            explanation_parts.append(
                "This role provides a low-barrier timeline that maps well with your budget flexibility."
            )
            
        explanation = " ".join(explanation_parts)
        
        matched_careers.append({
            "id": career["id"],
            "name": career["name"],
            "score": round(total_score, 1),
            "base_score": round(base_match_score, 1),
            "tag_bonus": round(bonus_tags, 1),
            "driver_bonus": round(driver_bonus, 1),
            "barrier_adjustment": round(barrier_adjustment + low_flex_boost, 1),
            "final_score": round(total_score, 1),
            "explanation": explanation,
            "salary": f"${career['salary']:,}",
            "growth": career["growth"],
            "riasec": career["riasec"],
            "description": career["description"],
            "high_barrier": career.get("high_barrier", False),
            "milestones": career.get("milestones", [])
        })
        
    # Sort matches by score descending
    matched_careers.sort(key=lambda x: x["score"], reverse=True)
    
    # 7. MATCH THE WIDER O*NET POOL
    top_curated_score = matched_careers[0]["score"] if matched_careers else 0.0
    secondary_results = []
    
    # Set of already matched SOC codes to avoid duplicate recommendations
    curated_soc_codes = set(CURATED_SOC_MAPPING.values())
    
    for soc_code, onet_career in ONET_DB.items():
        if soc_code in curated_soc_codes:
            continue
            
        # Calculate O*NET occupation RIASEC base match score
        total_dist = 0
        career_riasec = onet_career["riasec"]
        valid_dims = 0
        for dim in dimensions:
            u_val = parsed_user_riasec.get(dim)
            if u_val is not None:
                c_val = career_riasec.get(dim, 5.0)
                total_dist += abs(c_val - u_val)
                valid_dims += 1
                
        if valid_dims > 0:
            riasec_score = 1.0 - (total_dist / (valid_dims * 10.0))
        else:
            riasec_score = 1.0
        onet_base_score = riasec_score * 100.0
        
        # If this occupation scores strictly higher than the top curated career
        if onet_base_score > top_curated_score:
            secondary_results.append({
                "soc_code": soc_code,
                "title": onet_career["title"],
                "score": round(onet_base_score, 1)
            })
            
    # Sort and take top 5 secondary results
    secondary_results.sort(key=lambda x: x["score"], reverse=True)
    secondary_results = secondary_results[:5]
    
    # Extract self-judgement and transparency data for Phase 2 metrics
    self_judgement = data.get('self_judgement', {})
    self_creativity = float(self_judgement.get('creativity', 5.0))
    self_analytical = float(self_judgement.get('analytical', 5.0))
    self_social = float(self_judgement.get('social', 5.0))
    
    transparency = data.get('transparency', True)
    
    # Calculate computed counterparts
    def get_computed_value(val1, val2):
        vals = [v for v in [val1, val2] if v is not None]
        if not vals:
            return 5.0
        return sum(vals) / len(vals)

    computed_creativity = get_computed_value(parsed_user_riasec.get('A'), parsed_user_riasec.get('R'))
    computed_analytical = get_computed_value(parsed_user_riasec.get('I'), parsed_user_riasec.get('C'))
    computed_social = get_computed_value(parsed_user_riasec.get('S'), parsed_user_riasec.get('E'))
    
    # Absolute difference vector calculation
    diff = abs(self_creativity - computed_creativity) + \
           abs(self_analytical - computed_analytical) + \
           abs(self_social - computed_social)
           
    # Normalise difference to percentage alignment
    alignment_pct = round((1.0 - (diff / 30.0)) * 100.0, 1)
    
    return jsonify({
        "success": True,
        "results": matched_careers,
        "secondary_results": secondary_results,
        "alignment_percentage": alignment_pct,
        "transparency": transparency,
        "total_evaluated": len(CAREERS_DB)
    })

if __name__ == '__main__':
    # Bind to port specified by PORT env var for Render compatibility
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
