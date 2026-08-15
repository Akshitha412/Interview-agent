# 🚀 Interview Agent

An AI-powered adaptive technical interviewer that conducts real-time technical interviews, evaluates candidate answers, identifies skill gaps, and generates a personalized hiring-style assessment.

**Role + Skills + Experience → Adaptive Interview → Evaluation → Hiring Recommendation**

---

## Table of Contents

- [Why This Agent?](#-why-this-agent)
- [Key Features](#-key-features)
- [How the Agent Works](#how-the-agent-works)
- [Experience Levels](#experience-levels)
- [Architecture](#architecture)
- [What Makes It Different](#what-makes-it-different)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Agent](#running-the-agent)
- [Offline Mock Mode](#offline-mock-mode-no-api-key--no-network-required)
- [Project Structure](#project-structure)
- [Multi-line Answers](#multi-line-answers)
- [Sample Session](#sample-session)
- [Final Assessment](#final-assessment-example)

---

## 🎯 Why This Agent?

Traditional mock interview systems usually follow a fixed, linear pattern:

```
Question 1 → Question 2 → Question 3 → Final Score
```

Interview Agent replaces that with a real evaluation loop. The system isn't simply:

```
Prompt → LLM → Answer
```

Instead, it maintains a complete interview workflow:

```
Configure
   ↓
Generate Questions
   ↓
Ask Question
   ↓
Collect Answer
   ↓
Evaluate Answer
   ↓
Record Score + Feedback
   ↓
Continue Interview
   ↓
Aggregate Performance
   ↓
Generate Candidate Assessment
   ↓
Save Interview Report
```

```
                    ┌──────────────────────┐
                    │      CANDIDATE       │
                    └──────────┬───────────┘
                               │
                    Role + Skills + Experience
                               │
                               ▼
                    ┌──────────────────────┐
                    │   AI INTERVIEWER     │
                    │                      │
                    │ Generate → Ask       │
                    │      ↓               │
                    │ Evaluate Answer      │
                    │      ↓               │
                    │ Adapt Next Question  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  CANDIDATE PROFILE   │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
           ┌────────┐   ┌────────────┐  ┌────────────┐
           │ SCORE  │   │ STRENGTHS  │  │    GAPS    │
           └────────┘   └────────────┘  └────────────┘
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    RECOMMENDATION    │
                    │ Ready / Improve /    │
                    │ Not Recommended      │
                    └──────────────────────┘
```

---

## ⭐ Key Features

| Feature | What It Does |
|---|---|
| 🤖 **AI Question Generation** | Generates role-specific technical questions |
| 🎯 **Experience Awareness** | Fresher / Intermediate / Advanced |
| 🔄 **Adaptive Interview** | Adapts the interview based on candidate responses |
| 💬 **Interactive Interview** | Conducts the interview directly in the CLI |
| 📝 **Multi-line Answers** | Supports coding and detailed responses |
| ⚡ **Instant Evaluation** | Scores every answer immediately |
| 📊 **Final Assessment** | Calculates an overall interview score |
| 🔍 **Gap Detection** | Identifies areas requiring improvement |
| 🏁 **Recommendation** | Provides a hiring-style recommendation |
| 💾 **Persistent Sessions** | Saves JSON + Markdown transcripts |
| 🧪 **Mock Mode** | Runs without API/network |
| 📁 **Reproducible Mode** | Supports predefined answer files |

---

## How the Agent Works

```
                 CANDIDATE SETUP
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        Role         Skills     Experience
                                      │
                                      ▼
                           ┌─────────────────┐
                           │ QUESTION ENGINE │
                           └────────┬────────┘
                                    │
                                    ▼
                              Interview Q1
                                    │
                                    ▼
                              Candidate Answer
                                    │
                                    ▼
                           ┌─────────────────┐
                           │  AI EVALUATOR   │
                           └────────┬────────┘
                                    │
                              Score + Feedback
                                    │
                                    ▼
                              Interview Q2
                                    │
                                    ▼
                                  ...
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ FINAL ANALYZER  │
                           └────────┬────────┘
                                    │
             ┌──────────────────────┼──────────────────┐
             ▼                      ▼                  ▼
        Overall Score           Strengths            Gaps
                                    │
                                    ▼
                              Recommendation
                                    │
                                    ▼
                         JSON + Markdown Report
```

---

## Experience Levels

The candidate selects an experience level before starting the interview. This level is passed to the LLM so that generated questions match the candidate's expected depth.

| Level | Intended Focus |
|---|---|
| **Fresher** | Fundamentals, basic concepts, simple coding |
| **Intermediate** | Applied concepts, problem solving, practical scenarios |
| **Advanced** | System design, optimization, architecture, complex scenarios |

---

## Architecture

```
                    ┌───────────────┐
                    │ Candidate     │
                    │ Configuration │
                    └───────┬───────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ Question Generator │
                 │     LLM Call #1    │
                 └─────────┬──────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Interview Loop   │
                  │                  │
                  │ Q → Answer → Eval│
                  └────────┬─────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Answer Evaluator   │
                 │     LLM Call       │
                 └─────────┬──────────┘
                           │
                    Score + Feedback
                           │
                           ▼
                 ┌────────────────────┐
                 │ Final Evaluator    │
                 │     LLM Call       │
                 └─────────┬──────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Candidate Report│
                  └────────┬────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                  JSON          Markdown
```

---

## What Makes It Different

The project goes beyond a single LLM API call. The system maintains a **stateful workflow**, where the output of one stage becomes the input for the next:

```
Candidate Configuration
          ↓
Question Generation
          ↓
Candidate Answer
          ↓
Answer Evaluation
          ↓
Interview State
          ↓
Final Candidate Analysis
          ↓
Recommendation
```

This demonstrates:

- LLM orchestration across multiple calls
- Structured, schema-driven outputs
- Stateful, multi-turn workflow management
- Tool/API integration
- Automated evaluation
- Persistent, reproducible artifacts

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python |
| **LLM Provider** | Groq |
| **Model** | Llama 3.3 70B Versatile |
| **Interface** | CLI |
| **Configuration** | `.env` |
| **Structured Output** | JSON |
| **Persistence** | JSON + Markdown |
| **Testing** | Offline Mock Mode |

---

## Installation

**1. Clone the repository**

```bash
git clone <this-repo-url>
cd interview_agent
```

**2. Create a virtual environment**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your Groq API key**

Get a free key at [console.groq.com/keys](https://console.groq.com/keys), then copy `.env.example` to `.env` and add:

```
GROQ_API_KEY=your_groq_api_key_here
```

Requires **Python 3.9+**.

---

## Running the Agent

### Interactive mode

```bash
python interview_agent.py
```

The agent will prompt you for:

- Role
- Skills
- Experience level
- Number of questions

```
==================================================
              AI INTERVIEW AGENT
==================================================

Enter your role: Python Developer
Enter your skills (comma separated): Python, SQL, Flask

Select your experience level:
1. Fresher
2. Intermediate
3. Advanced
Enter choice (1-3): 2

How many questions? [default: 5]: 5
```

---

## Offline Mock Mode (no API key / no network required)

The project includes a mock mode for testing the complete workflow — question loop → scoring → final evaluation — without calling any LLM at all. It uses a simple local heuristic instead of real language understanding, so it's meant for testing the code path, not for judging answer quality:

```bash
python interview_agent.py \
    --role "Data Analyst" \
    --skills "SQL, Python, Statistics" \
    --num-questions 5 \
    --answers-file sample_output/sample_answers.json \
    --mock
```

Every run — mock or live — writes a timestamped transcript to `sessions/<timestamp>_<role>.json` and `sessions/<timestamp>_<role>.md`.

---

## Project Structure

```
interview_agent/
│
├── interview_agent.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── sample_output/
│   ├── sample_answers.json
│   ├── sample_transcript.md
│   └── sample_transcript.json
│
└── sessions/
    └── <generated-interview-sessions>
```

---

## Multi-line Answers

Coding questions aren't restricted to a single line. Type your full answer, then submit with `:submit` on its own line:

```
Q1: Write a Python function to calculate the total of a list.

Type your answer below.
Press ':submit' on a new line when you are finished.

> def calculate_total(items):
>     total = 0
>     for item in items:
>         total += item
>     return total
> :submit
```

The answer is then evaluated immediately:

```
→ Score: 8/10
→ Feedback: Strong implementation...
```

---

## Sample Session

```
==================================================
                AI INTERVIEW AGENT
==================================================

Enter your role: PYTHON
Enter your skills (comma separated): python

Select your experience level:
1. Fresher
2. Intermediate
3. Advanced
Enter choice (1-3): 2

How many questions? [default: 5]: 3

--------------------------------------------------
INTERVIEW CONFIGURATION
--------------------------------------------------
Role             : PYTHON
Skills           : python
Experience Level : Intermediate
Questions        : 3
--------------------------------------------------

Start interview? (y/n): y

=== Interview Agent === role='PYTHON' skills='python' level='Intermediate' n=3 mode=llama-3.3-70b-versatile
Generating questions...

Q1: How do you handle errors and exceptions in Python, and can
    you give an example of a try/except block you've used in a
    recent project?

> A try block holds code that might raise an error. The except
> block runs if an error occurs, and Python skips the rest of
> the try block. An else clause runs only if the try block
> completes without error. Example: division by zero.
> :submit

→ Score: 6/10
→ Feedback: Solid grasp of try/except/else, but the answer would
  benefit from an actual code example and a concrete project
  scenario rather than a general description.

Q2: Describe a situation where you had to optimize the
    performance of a Python script — what steps did you take,
    and what were the results?

> I identified the slow parts of the code, reduced unnecessary
> loops, used built-in functions, and avoided repeated database
> queries. After testing, the script ran faster and used less
> memory.
> :submit

→ Score: 6/10
→ Feedback: Good identification of optimization techniques, but
  the answer lacks measurable results (e.g., % improvement in
  speed or memory).

Q3: Can you explain the difference between static and dynamic
    typing, and how does Python's dynamic typing affect the way
    you design and write code?

> Static typing checks types before the program runs; dynamic
> typing determines them at runtime. Python is dynamically
> typed, so I don't need to declare variable types explicitly,
> which makes the language more flexible.
> :submit

→ Score: 4/10
→ Feedback: Correctly identifies Python as dynamically typed,
  but the explanation is brief and would benefit from concrete
  examples of how this affects code design.

Computing final evaluation...
```

---

## Final Assessment (Example)

```
==================================================
             FINAL EVALUATION
==================================================

Role: PYTHON
Skills: python
Experience Level: Intermediate

Overall Score: 5.33/10

Strengths:
✓ Basic understanding of try/except blocks
✓ Ability to identify key steps for optimizing Python script performance

Gaps:
✗ Lack of concrete examples from recent projects
✗ Limited understanding of static and dynamic typing
✗ Needs improvement in code syntax and explanation clarity

Recommendation:
Needs Improvement
```

---

