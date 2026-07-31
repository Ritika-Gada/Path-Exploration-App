require 'webrick'
require 'json'

PORT = 5001

CAREERS_DB = [
  {
    "id" => "prompt_engineer",
    "name" => "Prompt Engineer",
    "riasec" => {"R" => 2, "I" => 9, "A" => 7, "S" => 4, "E" => 6, "C" => 5},
    "tags" => ["coding", "writing", "remote-work", "creative-design", "research"],
    "required_tags" => ["writing"],
    "salary" => 125000,
    "growth" => "Explosive",
    "driver" => "Passion",
    "intents" => ["Full-time", "Part-time", "Hobby"],
    "high_barrier" => false,
    "description" => "Designs and refines AI prompts to achieve optimal responses from large language models, bridging human intent and AI execution.",
    "milestones" => [
      {
        "id" => 1,
        "title" => "LLM Settings & System Prompts",
        "description" => "Learn how settings like Temperature, Top P, and System Prompts govern model output randomness and behavioral constraints.",
        "resource_label" => "Guide to LLM Parameters",
        "resource_url" => "https://promptingguide.ai/introduction/settings",
        "quiz" => {
          "questions" => [
            {
              "question" => "What is the primary effect of increasing the Temperature parameter in an LLM?",
              "options" => ["It increases output creativity and randomness", "It speeds up inference time", "It makes the model stick strictly to facts", "It increases context window size"],
              "answer" => 0,
              "explanation" => "Temperature controls randomness: higher values (close to 1.0) increase diversity/creativity, while lower values make it deterministic."
            },
            {
              "question" => "Which type of prompt establishes the overall persona and rules that a model must follow throughout a conversation?",
              "options" => ["User Prompt", "Few-Shot Prompt", "System Prompt", "Chained Prompt"],
              "answer" => 2,
              "explanation" => "System prompts set the guidelines, tone, constraints, and instructions for how the model responds to any subsequent user prompts."
            }
          ]
        }
      },
      {
        "id" => 2,
        "title" => "Few-Shot Prompting Patterns",
        "description" => "Master the art of giving in-context examples to help the model learn complex formatting and reasoning behaviors without retraining.",
        "resource_label" => "Few-Shot Prompting Guide",
        "resource_url" => "https://promptingguide.ai/techniques/fewshot",
        "quiz" => {
          "questions" => [
            {
              "question" => "What is the key difference between Zero-Shot and Few-Shot prompting?",
              "options" => ["Few-Shot contains examples, Zero-Shot does not", "Zero-Shot requires custom python code", "Few-Shot increases model inference speed", "Few-Shot updates the model's core weights"],
              "answer" => 0,
              "explanation" => "Few-Shot prompting provides one or more examples of inputs and desired outputs inside the prompt, whereas Zero-Shot has none."
            },
            {
              "question" => "When structure matching (e.g. outputting valid JSON), which prompting technique is most reliable?",
              "options" => ["Asking nicely", "Few-Shot format exemplars", "Increasing Temperature", "Using shorter prompts"],
              "answer" => 1,
              "explanation" => "Providing clear structured examples (few-shot) establishes the pattern for the LLM to reproduce exactly."
            }
          ]
        }
      },
      {
        "id" => 3,
        "title" => "Prompt Chaining & Security",
        "description" => "Build pipelines that link multiple LLM calls together, and learn strategies to defend against prompt injection vulnerabilities.",
        "resource_label" => "Prompt Security and Defenses",
        "resource_url" => "https://promptingguide.ai/adversarial/adversarial-prompting",
        "quiz" => {
          "questions" => [
            {
              "question" => "What occurs during a Prompt Injection attack?",
              "options" => ["Untrusted user input overrides the developer instructions", "The model's API server crashes", "The model starts writing slow code", "The cost per token increases"],
              "answer" => 0,
              "explanation" => "Prompt injection happens when user inputs trick the LLM into ignoring system rules to perform unintended actions."
            },
            {
              "question" => "Why is 'Prompt Chaining' used in complex workflows?",
              "options" => ["It reduces API cost", "It breaks down a complex task into smaller, highly controlled sequential steps", "It bypasses prompt size limits", "It trains the model offline"],
              "answer" => 1,
              "explanation" => "Chaining breaks a big problem into steps where the output of one prompt feed as input to the next, enhancing output accuracy."
            }
          ]
        }
      }
    ]
  },
  {
    "id" => "mlops_specialist",
    "name" => "MLOps Specialist",
    "riasec" => {"R" => 6, "I" => 9, "A" => 3, "S" => 3, "E" => 5, "C" => 8},
    "tags" => ["coding", "data-analysis", "remote-work", "security"],
    "required_tags" => ["coding"],
    "salary" => 155000,
    "growth" => "High",
    "driver" => "Money",
    "intents" => ["Full-time"],
    "high_barrier" => true,
    "description" => "Deploys, monitors, and maintains machine learning models in production, ensuring system reliability and scalability.",
    "milestones" => [
      {
        "id" => 1,
        "title" => "Docker Containerization for ML",
        "description" => "Package models, code, and dependencies into reproducible Docker containers to ensure consistent execution environment.",
        "resource_label" => "Docker for Machine Learning",
        "resource_url" => "https://docs.docker.com/get-started/",
        "quiz" => {
          "questions" => [
            {
              "question" => "What is the primary benefit of containerizing an ML model?",
              "options" => ["It guarantees the model runs in the exact same environment anywhere", "It automatically retrains the model", "It compresses model weights", "It writes inference code"],
              "answer" => 0,
              "explanation" => "Docker ensures that code, OS, Python libraries, and model weights are packaged identically, avoiding the 'works on my machine' issue."
            },
            {
              "question" => "Which Docker file instruction sets up the dependencies to run?",
              "options" => ["RUN", "EXPOSE", "COPY", "FROM"],
              "answer" => 0,
              "explanation" => "The RUN command executes setup steps in the image, such as 'pip install -r requirements.txt'."
            }
          ]
        }
      },
      {
        "id" => 2,
        "title" => "CI/CD Pipelines & Version Control",
        "description" => "Set up automated GitHub actions to run validation tests, check for performance degradation, and build containers automatically.",
        "resource_label" => "Continuous Integration in ML",
        "resource_url" => "https://github.com/features/actions",
        "quiz" => {
          "questions" => [
            {
              "question" => "What does CI/CD stand for in deployment pipelines?",
              "options" => ["Continuous Integration & Continuous Deployment", "Code Inspection & Cloud Delivery", "Calculated Inference & Coding Drive", "Critical Infrastructure & Container Deploy"],
              "answer" => 0,
              "explanation" => "CI/CD automates testing and deployment on new code updates to improve pipeline safety and speed."
            },
            {
              "question" => "Why is 'data versioning' crucial in ML systems compared to standard software?",
              "options" => ["Because datasets change and govern model behaviors", "Because code is not version controlled", "To minimize storage pricing", "To build fast databases"],
              "answer" => 0,
              "explanation" => "An ML model is code + data. Versioning the dataset (using tools like DVC) is necessary to reproduce training results."
            }
          ]
        }
      },
      {
        "id" => 3,
        "title" => "Data & Concept Drift Monitoring",
        "description" => "Build monitoring pipelines to log incoming data, audit accuracy trends, and flag when distribution patterns deviate from training sets.",
        "resource_label" => "Introduction to Model Drift",
        "resource_url" => "https://www.evidentlyai.com/ml-in-production/data-drift",
        "quiz" => {
          "questions" => [
            {
              "question" => "What is 'Data Drift'?",
              "options" => ["The statistical distribution of model input variables changes over time", "A databases server runs out of disk space", "Network packets dropping during model inference", "The model's parameters changing during runtime"],
              "answer" => 0,
              "explanation" => "Data drift happens when real-world production inputs change statistically from the historical dataset used to train the model."
            },
            {
              "question" => "How do you resolve Concept Drift in production?",
              "options" => ["Retrain the model on recent, labeled data", "Decrease the temperature", "Restart the server", "Write simpler code"],
              "answer" => 0,
              "explanation" => "When the relationship between inputs and targets shift (concept drift), models must be retrained on newly captured production samples."
            }
          ]
        }
      }
    ]
  },
  {
    "id" => "ux_ui_designer",
    "name" => "UX/UI Designer",
    "riasec" => {"R" => 2, "I" => 6, "A" => 10, "S" => 6, "E" => 5, "C" => 4},
    "tags" => ["creative-design", "remote-work", "client-interaction", "writing"],
    "required_tags" => ["creative-design"],
    "salary" => 95000,
    "growth" => "High",
    "driver" => "Passion",
    "intents" => ["Full-time", "Part-time", "Hobby"],
    "high_barrier" => false,
    "description" => "Creates intuitive, user-friendly, and visually stunning digital interfaces, focusing on user journeys and interactive prototypes.",
    "milestones" => [
      {
        "id" => 1,
        "title" => "Figma Basics & Auto Layout",
        "description" => "Learn layout grids, component structures, and the power of Auto Layout to create highly responsive screen designs.",
        "resource_label" => "Learn Figma Auto Layout",
        "resource_url" => "https://help.figma.com/hc/en-us/articles/360040451373-Create-dynamic-layouts-with-Auto-layout",
        "quiz" => {
          "questions" => [
            {
              "question" => "What is the primary benefit of Figma's Auto Layout?",
              "options" => ["Designs adjust automatically when text or spacing shifts", "It converts designs directly to production HTML/CSS", "It automatically selects visual color palettes", "It edits vectors automatically"],
              "answer" => 0,
              "explanation" => "Auto layout lets you create frames that shrink or grow response to content, similar to flexbox in CSS."
            },
            {
              "question" => "Which constraint setting allows an item to fill the width of its parent container?",
              "options" => ["Hug contents", "Fixed width", "Fill container", "Align stretch"],
              "answer" => 2,
              "explanation" => "'Fill container' expands elements to utilize all available width/height allocated by the parent Auto Layout frame."
            }
          ]
        }
      },
      {
        "id" => 2,
        "title" => "Wireframes & Interactive Flows",
        "description" => "Build low-fidelity visual sketches, plan user navigation journeys, and link screens into clickable interactive flows.",
        "resource_label" => "UI Wireframing & Flow Design",
        "resource_url" => "https://www.nngroup.com/articles/wireflows/",
        "quiz" => {
          "questions" => [
            {
              "question" => "What is the goal of low-fidelity wireframing?",
              "options" => ["Focus on structural layouts without getting distracted by visual polish", "Test API data transmission speeds", "Add final animations and typography styling", "Build product marketing pages"],
              "answer" => 0,
              "explanation" => "Low-fidelity wireframes focus on visual layout hierarchy, functionality, and flow, omitting colors, fonts, and assets."
            },
            {
              "question" => "Why do designers build interactive prototypes?",
              "options" => ["To test workflows and gather feedback before coding", "To measure backend load speeds", "To compile assets for production databases", "To automate developer commits"],
              "answer" => 0,
              "explanation" => "Clickable prototypes simulate interactions, allowing user experience teams to validate design logic and collect early feedback."
            }
          ]
        }
      },
      {
        "id" => 3,
        "title" => "Design Systems & Visual Hierarchy",
        "description" => "Create global design tokens for colors, typography, buttons, and form states to ensure consistency across product interfaces.",
        "resource_label" => "Introduction to Design Systems",
        "resource_url" => "https://www.uxpin.com/studio/blog/design-systems-guide/",
        "quiz" => {
          "questions" => [
            {
              "question" => "What elements establish visual hierarchy on a screen?",
              "options" => ["Contrasting scale, color contrast, and empty spacing", "Adding more icons", "Centering all text fields", "Using the default operating system fonts"],
              "answer" => 0,
              "explanation" => "Scale, font weights, high-contrast colors, and layout whitespace guide the user's focus through the interface elements."
            },
            {
              "question" => "What is a major advantage of utilizing a component-driven Design System?",
              "options" => ["Changes to a master component sync globally to all instances", "It replaces the need for code implementation", "It automatically uploads to git", "It decreases the designer's pay rate"],
              "answer" => 0,
              "explanation" => "Design systems establish master components (buttons, headers), ensuring changes cascade globally, maintaining complete UI consistency."
            }
          ]
        }
      }
    ]
  },
  # Adding the other main careers with shorter structure for file space, keeping prompt_engineer, mlops, ux_ui fully complete, and others functional
  {
    "id" => "digital_content_strategist",
    "name" => "Digital Content Strategist",
    "riasec" => {"R" => 1, "I" => 5, "A" => 9, "S" => 6, "E" => 7, "C" => 4},
    "tags" => ["creative-design", "writing", "remote-work", "client-interaction"],
    "required_tags" => ["writing", "creative-design"],
    "salary" => 85000,
    "growth" => "High",
    "driver" => "Passion",
    "intents" => ["Full-time", "Part-time", "Hobby"],
    "high_barrier" => false,
    "description" => "Develops and executes multi-channel content strategies, overseeing creation of visual and written media assets.",
    "milestones" => [
      {
        "id" => 1,
        "title" => "SEO Foundations",
        "description" => "Master keyword research tools, plan semantic architectures, and outline content briefs.",
        "resource_label" => "SEO Keyword Strategy Guide",
        "resource_url" => "https://moz.com/beginners-guide-to-seo",
        "quiz" => {
          "questions" => [
            {
              "question" => "What does an SEO content brief specify?",
              "options" => ["Keywords, user intent, content outline, and visual suggestions", "Full HTML templates", "Server database ports", "Contract billing margins"],
              "answer" => 0,
              "explanation" => "Content briefs align creators on keywords, user intent, and header hierarchy."
            },
            {
              "question" => "Which metric evaluates search query competitiveness?",
              "options" => ["Keyword Difficulty", "Domain Authority", "Click-through rate", "Search impressions"],
              "answer" => 0,
              "explanation" => "Keyword Difficulty predicts how hard it is to rank on page 1 for a search phrase."
            }
          ]
        }
      }
    ]
  }
]

# Quick fallback for other IDs to prevent crashes in server.rb if they don't have custom milestones
ALL_CAREER_IDS = [
  "growth_marketer", "data_analyst", "product_manager", "devrel_engineer",
  "sustainability_consultant", "cybersecurity_analyst", "blockchain_developer",
  "ai_ethicist", "customer_success_manager", "talent_acquisition_partner",
  "agile_scrum_master", "fintech_financial_planner", "healthcare_informatics_specialist",
  "ecommerce_brand_manager"
]

# Generate simple placeholder milestones if not fully declared in Ruby DB to keep code small
CAREERS_DB.each do |c|
  next if c["milestones"] && !c["milestones"].empty?
  c["milestones"] = [
    {
      "id" => 1,
      "title" => "Foundational Training & Concepts",
      "description" => "Learn key paradigms, tools, and workflows standard in this professional domain.",
      "resource_label" => "Domain Overview Guide",
      "resource_url" => "https://google.com/",
      "quiz" => {
        "questions" => [
          {
            "question" => "What represents the main goal of this foundation phase?",
            "options" => ["Master key baseline terms and systems", "Write complex production code", "Invest capital in advertisements", "Manage large cross-functional teams"],
            "answer" => 0,
            "explanation" => "Understanding vocabulary and system basics is standard before doing advanced operations."
          },
          {
            "question" => "Why do professionals audit their workflows continuously?",
            "options" => ["To minimize friction and align execution with targets", "To decrease team salaries", "To avoid remote work opportunities", "To change system fonts"],
            "answer" => 0,
            "explanation" => "Continuous process alignment ensures high productivity and correct outcomes."
          }
        ]
      }
    },
    {
      "id" => 2,
      "title" => "Micro-Project Portfolio Piece",
      "description" => "Build a mock simulation or sandbox asset demonstrating practical skills to recruiters.",
      "resource_label" => "Portfolio Project Sandbox",
      "resource_url" => "https://github.com/",
      "quiz" => {
        "questions" => [
          {
            "question" => "What is the role of a portfolio micro-project?",
            "options" => ["Demonstrate hands-on capabilities to stakeholders", "Secure venture funding", "Replace core production apps", "Avoid documentation writing"],
            "answer" => 0,
            "explanation" => "Micro-projects serve as tangible proof of skills for career changers."
          },
          {
            "question" => "What is a best practice when presenting project portfolios?",
            "options" => ["Clearly document the problem, solution details, and clean outputs", "Show only folders of messy code", "Hide all descriptions", "State that it took a year to build"],
            "answer" => 0,
            "explanation" => "Clear READMEs detailing constraints, methods, and outcomes make projects readable for recruiters."
          }
        ]
      }
    }
  ]
end

# Add other missing careers to keep DB in parity with app.py
RAW_OTHER_CAREERS = [
  {"id" => "growth_marketer", "name" => "Growth Marketer", "riasec" => {"R" => 1, "I" => 7, "A" => 6, "S" => 6, "E" => 9, "C" => 5}, "tags" => ["data-analysis", "client-interaction", "writing", "leadership", "remote-work"], "required_tags" => ["client-interaction"], "salary" => 88000, "growth" => "Steady", "driver" => "Balance", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Drives user acquisition through data-driven campaigns and marketing funnel optimization."},
  {"id" => "data_analyst", "name" => "Data Analyst", "riasec" => {"R" => 2, "I" => 8, "A" => 3, "S" => 4, "E" => 5, "C" => 9}, "tags" => ["data-analysis", "remote-work", "writing", "coding"], "required_tags" => ["data-analysis"], "salary" => 82000, "growth" => "Steady", "driver" => "Balance", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Transforms raw data into actionable insights, dashboards, and reported statistics."},
  {"id" => "product_manager", "name" => "Product Manager", "riasec" => {"R" => 2, "I" => 6, "A" => 5, "S" => 8, "E" => 10, "C" => 6}, "tags" => ["leadership", "client-interaction", "writing", "data-analysis"], "required_tags" => ["leadership", "client-interaction"], "salary" => 135000, "growth" => "High", "driver" => "Money", "intents" => ["Full-time"], "high_barrier" => true, "description" => "Defines product vision and strategy, aligns cross-functional engineering, design, and roadmap goals."},
  {"id" => "devrel_engineer", "name" => "DevRel Engineer", "riasec" => {"R" => 3, "I" => 7, "A" => 7, "S" => 9, "E" => 8, "C" => 4}, "tags" => ["coding", "public-speaking", "client-interaction", "writing", "remote-work"], "required_tags" => ["coding", "public-speaking"], "salary" => 120000, "growth" => "High", "driver" => "Passion", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Bridges the gap between external developers and internal engineering teams via documentation and tutorials."},
  {"id" => "sustainability_consultant", "name" => "Sustainability Consultant", "riasec" => {"R" => 3, "I" => 8, "A" => 4, "S" => 8, "E" => 7, "C" => 6}, "tags" => ["client-interaction", "research", "writing", "leadership"], "required_tags" => ["client-interaction"], "salary" => 92000, "growth" => "High", "driver" => "Balance", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Advises organizations on minimizing environmental footprint and adopting carbon reduction practices."},
  {"id" => "cybersecurity_analyst", "name" => "Cybersecurity Analyst", "riasec" => {"R" => 5, "I" => 9, "A" => 2, "S" => 4, "E" => 4, "C" => 9}, "tags" => ["security", "coding", "remote-work", "data-analysis"], "required_tags" => ["security"], "salary" => 112000, "growth" => "Very High", "driver" => "Money", "intents" => ["Full-time"], "high_barrier" => true, "description" => "Protects organizational network and system integrity from cyber threats, monitoring logs and firewall logs."},
  {"id" => "blockchain_developer", "name" => "Blockchain Developer", "riasec" => {"R" => 4, "I" => 9, "A" => 4, "S" => 2, "E" => 6, "C" => 8}, "tags" => ["coding", "security", "remote-work", "data-analysis", "research"], "required_tags" => ["coding"], "salary" => 145000, "growth" => "Steady", "driver" => "Money", "intents" => ["Full-time", "Part-time", "Hobby"], "high_barrier" => true, "description" => "Designs and builds decentralized protocols, smart contracts, and architecture."},
  {"id" => "ai_ethicist", "name" => "AI Ethicist", "riasec" => {"R" => 1, "I" => 9, "A" => 7, "S" => 8, "E" => 5, "C" => 6}, "tags" => ["research", "writing", "public-speaking", "remote-work", "client-interaction"], "required_tags" => ["research", "writing"], "salary" => 105000, "growth" => "Emerging", "driver" => "Passion", "intents" => ["Full-time", "Part-time", "Hobby"], "high_barrier" => false, "description" => "Evaluates societal, moral, and regulatory impacts of AI systems, establishing safety frameworks."},
  {"id" => "customer_success_manager", "name" => "Customer Success Manager", "riasec" => {"R" => 1, "I" => 4, "A" => 4, "S" => 9, "E" => 8, "C" => 6}, "tags" => ["client-interaction", "remote-work", "writing", "leadership"], "required_tags" => ["client-interaction"], "salary" => 78000, "growth" => "Steady", "driver" => "Balance", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Partners with SaaS customers to guide onboarding, prevent churn, and drive long-term business retention."},
  {"id" => "talent_acquisition_partner", "name" => "Talent Acquisition Partner", "riasec" => {"R" => 1, "I" => 4, "A" => 4, "S" => 9, "E" => 8, "C" => 6}, "tags" => ["client-interaction", "leadership", "writing", "remote-work"], "required_tags" => ["client-interaction"], "salary" => 80000, "growth" => "Steady", "driver" => "Balance", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Identifies, recruits, and builds relationships with top professional talent, designing pipelines."},
  {"id" => "agile_scrum_master", "name" => "Agile Scrum Master", "riasec" => {"R" => 2, "I" => 5, "A" => 3, "S" => 9, "E" => 7, "C" => 8}, "tags" => ["leadership", "client-interaction", "remote-work", "data-analysis"], "required_tags" => ["leadership"], "salary" => 105000, "growth" => "High", "driver" => "Balance", "intents" => ["Full-time"], "high_barrier" => true, "description" => "Facilitates agile team sprints, coaching cross-functional teams on scrum methodology."},
  {"id" => "fintech_financial_planner", "name" => "Fintech Financial Planner", "riasec" => {"R" => 2, "I" => 7, "A" => 2, "S" => 6, "E" => 8, "C" => 9}, "tags" => ["data-analysis", "client-interaction", "remote-work", "security"], "required_tags" => ["data-analysis", "client-interaction"], "salary" => 115000, "growth" => "High", "driver" => "Money", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Advises individuals and organizations on financial strategy, utilizing modern algorithmic planning."},
  {"id" => "healthcare_informatics_specialist", "name" => "Healthcare Informatics Specialist", "riasec" => {"R" => 4, "I" => 8, "A" => 2, "S" => 6, "E" => 4, "C" => 8}, "tags" => ["data-analysis", "remote-work", "writing", "security"], "required_tags" => ["data-analysis"], "salary" => 98000, "growth" => "Very High", "driver" => "Balance", "intents" => ["Full-time"], "high_barrier" => false, "description" => "Bridges healthcare workflows and database systems, auditing health records flow."},
  {"id" => "ecommerce_brand_manager", "name" => "E-commerce Brand Manager", "riasec" => {"R" => 2, "I" => 6, "A" => 6, "S" => 5, "E" => 9, "C" => 7}, "tags" => ["leadership", "data-analysis", "creative-design", "remote-work", "client-interaction"], "required_tags" => ["leadership"], "salary" => 90000, "growth" => "Steady", "driver" => "Money", "intents" => ["Full-time", "Part-time"], "high_barrier" => false, "description" => "Manages digital retail storefronts, inventory, and brand marketing funnels."}
]

# Inject default placeholders for other entries to avoid duplication code size
RAW_OTHER_CAREERS.each do |c|
  # Skip if already exists
  next if CAREERS_DB.any? { |db_c| db_c["id"] == c["id"] }
  
  c["milestones"] = [
    {
      "id" => 1,
      "title" => "Foundational Training & Concepts",
      "description" => "Learn key paradigms, tools, and workflows standard in this professional domain.",
      "resource_label" => "Domain Overview Guide",
      "resource_url" => "https://google.com/",
      "quiz" => {
        "questions" => [
          {
            "question" => "What represents the main goal of this foundation phase?",
            "options" => ["Master key baseline terms and systems", "Write complex production code", "Invest capital in advertisements", "Manage large cross-functional teams"],
            "answer" => 0,
            "explanation" => "Understanding vocabulary and system basics is standard before doing advanced operations."
          },
          {
            "question" => "Why do professionals audit their workflows continuously?",
            "options" => ["To minimize friction and align execution with targets", "To decrease team salaries", "To avoid remote work opportunities", "To change system fonts"],
            "answer" => 0,
            "explanation" => "Continuous process alignment ensures high productivity and correct outcomes."
          }
        ]
      }
    },
    {
      "id" => 2,
      "title" => "Micro-Project Portfolio Piece",
      "description" => "Build a mock simulation or sandbox asset demonstrating practical skills to recruiters.",
      "resource_label" => "Portfolio Project Sandbox",
      "resource_url" => "https://github.com/",
      "quiz" => {
        "questions" => [
          {
            "question" => "What is the role of a portfolio micro-project?",
            "options" => ["Demonstrate hands-on capabilities to stakeholders", "Secure venture funding", "Replace core production apps", "Avoid documentation writing"],
            "answer" => 0,
            "explanation" => "Micro-projects serve as tangible proof of skills for career changers."
          },
          {
            "question" => "What is a best practice when presenting project portfolios?",
            "options" => ["Clearly document the problem, solution details, and clean outputs", "Show only folders of messy code", "Hide all descriptions", "State that it took a year to build"],
            "answer" => 0,
            "explanation" => "Clear READMEs detailing constraints, methods, and outcomes make projects readable for recruiters."
          }
        ]
      }
    }
  ]
  CAREERS_DB << c
end

class WebServer < WEBrick::HTTPServlet::AbstractServlet
  def do_GET(request, response)
    path = request.path

    if path == "/"
      response.status = 200
      response.content_type = "text/html"
      response.body = File.read(File.join(__dir__, 'templates', 'index.html'))
    elsif path == "/static/css/style.css"
      response.status = 200
      response.content_type = "text/css"
      response.body = File.read(File.join(__dir__, 'static', 'css', 'style.css'))
    else
      response.status = 404
      response.content_type = "text/plain"
      response.body = "Not Found"
    end
  end

  def do_POST(request, response)
    if request.path == "/api/match"
      begin
        data = JSON.parse(request.body) || {}
        
        user_riasec = data['riasec'] || {}
        likes = data['likes'] || []
        dislikes = data['dislikes'] || []
        intent = data['intent'] || 'Full-time'
        driver = data['driver'] || 'Passion'
        financial_flexibility = data['financial_flexibility'] || 'Medium' # 'Low', 'Medium', 'High'

        dimensions = ["R", "I", "A", "S", "E", "C"]
        parsed_user_riasec = {}
        dimensions.each do |dim|
          val = user_riasec[dim]
          if val.nil? || val == "" || val == "null"
            parsed_user_riasec[dim] = nil
          else
            parsed_user_riasec[dim] = val.to_f
          end
        end

        matched_careers = []

        CAREERS_DB.each do |career|
          # 1. HARD EXCLUSION: Dislikes
          exclude = false
          career["required_tags"].each do |req_tag|
            if dislikes.include?(req_tag)
              exclude = true
              break
            end
          end

          # 2. HARD EXCLUSION: Intent
          if !career["intents"].include?(intent)
            exclude = true
          end

          next if exclude

          # 3. RIASEC SCORE (handling skipped dimensions dynamically)
          active_dimensions = dimensions.select { |dim| !parsed_user_riasec[dim].nil? }
          if !active_dimensions.empty?
            total_dist = 0.0
            active_dimensions.each do |dim|
              c_val = (career["riasec"][dim] || 5.0).to_f
              u_val = parsed_user_riasec[dim]
              total_dist += (c_val - u_val).abs
            end
            riasec_score = 1.0 - (total_dist / (active_dimensions.length * 10.0))
          else
            riasec_score = 1.0
          end
          base_match_score = riasec_score * 100.0

          # 4. TAG BONUSES
          bonus_tags = 0.0
          matching_tags = []
          likes.each do |tag|
            if career["tags"].include?(tag)
              bonus_tags += 4.0
              matching_tags << tag
            end
          end

          # 5. DRIVER MATCH
          driver_bonus = 0.0
          if driver == career["driver"]
            driver_bonus = 10.0
          end

          # 6. FINANCIAL FLEXIBILITY AND BARRIER CONSTRAINT ADJUSTMENTS
          barrier_adjustment = 0.0
          if financial_flexibility == 'Low' && career["high_barrier"]
            barrier_adjustment = -15.0
          elsif financial_flexibility == 'High' && career["high_barrier"]
            barrier_adjustment = 5.0
          end

          low_flex_boost = 0.0
          if financial_flexibility == 'Low' && !career["high_barrier"] && ['Part-time', 'Hobby'].include?(intent)
            low_flex_boost = 10.0
          end

          total_score = base_match_score + bonus_tags + driver_bonus + barrier_adjustment + low_flex_boost
          total_score = [0.0, [100.0, total_score].min].max

          # Generate Dynamic explanation
          active_user_riasec = parsed_user_riasec.reject { |k, v| v.nil? }
          if !active_user_riasec.empty?
            sorted_user_traits = active_user_riasec.sort_by { |k, v| -v }
            dominant_trait_key = sorted_user_traits[0][0]
          else
            dominant_trait_key = "A"
          end
          
          trait_names = {
            "R" => "Realistic (Doer)",
            "I" => "Investigative (Thinker)",
            "A" => "Artistic (Creator)",
            "S" => "Social (Helper)",
            "E" => "Enterprising (Persuader)",
            "C" => "Conventional (Organizer)"
          }
          dominant_trait_name = trait_names[dominant_trait_key] || "creative"

          explanation_parts = []
          explanation_parts << "Your high affinity for #{dominant_trait_name} activities aligns well with the core workflows of a #{career['name']}."
          
          if !matching_tags.empty?
            formatted_tags = matching_tags.take(2).map { |t| t.gsub('-', ' ') }
            explanation_parts << "Your preferences for #{formatted_tags.join(', ')} match this role's environment."
          end

          if driver == career["driver"]
            explanation_parts << "It also perfectly caters to your primary motivator: #{driver}."
          end

          if financial_flexibility == 'Low' && career["high_barrier"]
            explanation_parts << "Note: Highly technical barriers require investment, which may conflict with your low financial flexibility."
          elsif financial_flexibility == 'Low' && !career["high_barrier"]
            explanation_parts << "This role provides a low-barrier timeline that maps well with your budget flexibility."
          end

          explanation = explanation_parts.join(" ")

          matched_careers << {
            "id" => career["id"],
            "name" => career["name"],
            "score" => total_score.round(1),
            "explanation" => explanation,
            "salary" => "$#{career['salary'].to_s.gsub(/(\d)(?=(\d\d\d)+(?!\d))/, '\\1,')}",
            "growth" => career["growth"],
            "riasec" => career["riasec"],
            "description" => career["description"],
            "high_barrier" => career["high_barrier"],
            "milestones" => career["milestones"]
          }
        end

        # Sort all matched careers descending
        matched_careers.sort_by! { |c| -c["score"] }

        self_judgement = data['self_judgement'] || {}
        self_creativity = (self_judgement['creativity'] || 5.0).to_f
        self_analytical = (self_judgement['analytical'] || 5.0).to_f
        self_social = (self_judgement['social'] || 5.0).to_f

        transparency = data.key?('transparency') ? data['transparency'] : true

        active_c = [parsed_user_riasec['A'], parsed_user_riasec['R']].compact
        computed_creativity = active_c.empty? ? 5.0 : active_c.sum / active_c.length.to_f

        active_a = [parsed_user_riasec['I'], parsed_user_riasec['C']].compact
        computed_analytical = active_a.empty? ? 5.0 : active_a.sum / active_a.length.to_f

        active_s = [parsed_user_riasec['S'], parsed_user_riasec['E']].compact
        computed_social = active_s.empty? ? 5.0 : active_s.sum / active_s.length.to_f

        diff = (self_creativity - computed_creativity).abs +
               (self_analytical - computed_analytical).abs +
               (self_social - computed_social).abs

        alignment_pct = ((1.0 - (diff / 30.0)) * 100.0).round(1)

        response.status = 200
        response.content_type = "application/json"
        response.body = JSON.generate({
          "success" => true,
          "results" => matched_careers,
          "alignment_percentage" => alignment_pct,
          "transparency" => transparency,
          "total_evaluated" => CAREERS_DB.length
        })
      rescue => e
        response.status = 500
        response.content_type = "application/json"
        response.body = JSON.generate({ "success" => false, "error" => e.message })
      end
    else
      response.status = 404
      response.content_type = "text/plain"
      response.body = "Not Found"
    end
  end
end

server = WEBrick::HTTPServer.new(:Port => PORT, :BindAddress => '127.0.0.1')
server.mount '/', WebServer

trap 'INT' do server.shutdown end
puts "Server started on http://127.0.0.1:#{PORT}"
server.start
