# Interview Agent

An AI-powered adaptive technical interviewer that evaluates candidates in real time, identifies skill gaps, and generates a personalized interview assessment.

Role + Skills + Experience → Adaptive Interview → Instant Evaluation → Hiring Recommendation

# Why This Agent?

Traditional mock interviews usually give you a fixed list of questions and a final score.

Interview Agent turns the interview itself into an evaluation loop.

It:

🎯 Generates questions based on role + skills + experience level
💬 Supports real interactive interviews
📝 Supports multi-line coding answers
⚡ Evaluates every answer immediately
🧠 Identifies strengths and knowledge gaps
📊 Produces an overall performance score
🎯 Gives a hiring-style recommendation
💾 Saves the complete interview as JSON + Markdown


##  The key idea

Candidate
    │
    │ Role + Skills + Experience
    ▼
┌─────────────────────────────┐
│     AI INTERVIEWER          │
│                             │
│ Generate → Ask → Evaluate   │
│      ↑              │       │
│      └──── Adapt ───┘       │
└─────────────────────────────┘
             │
             ▼
      Candidate Profile
             │
      ┌──────┼───────┐
      ▼      ▼       ▼
    Score  Strengths Gaps
             │
             ▼
       Recommendation


# | Feature                       | What it does                                |
| ----------------------------- | ------------------------------------------- |
| 🤖 **AI Question Generation** | Generates role-specific technical questions |
| 🎯 **Experience Awareness**   | Fresher / Intermediate / Advanced           |
| 💬 **Interactive Interview**  | Conducts the interview directly in the CLI  |
| 📝 **Multi-line Answers**     | Supports coding and detailed responses      |
| ⚡ **Instant Evaluation**      | Scores every answer immediately             |
| 📊 **Final Assessment**       | Calculates an overall interview score       |
| 🔍 **Gap Detection**          | Identifies areas requiring improvement      |
| 🎯 **Recommendation**         | Provides a hiring-style recommendation      |
| 💾 **Persistent Sessions**    | Saves JSON + Markdown transcripts           |
| 🧪 **Mock Mode**              | Runs without API/network                    |
| 📁 **Reproducible Mode**      | Supports predefined answer files            |
      

# HOW THE AGENT WORKS

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

## Interactive Interview
Run:
python interview_agent.py
The agent asks:
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

## Experience Levels

The candidate selects an experience level before the interview. The selected
level is provided to the LLM so that generated questions can be appropriate
to the candidate's experience.

| Level | Intended Focus |
|---|---|
| Fresher | Fundamentals, basic concepts, simple coding |
| Intermediate | Applied concepts, problem solving, practical scenarios |
| Advanced | System design, optimization, architecture, complex scenarios |

# Multi-line answers

Coding questions aren't restricted to one line.

Q1: Write a Python function to...


Type your answer below.
Press ':submit' on a new line when you are finished.


> def calculate_total(items):
>     total = 0
>     for item in items:
>         total += item
>     return total
> :submit


→ Score: 8/10
→ Feedback: Strong implementation...

his is a great feature to demonstrate, so keep it prominent

# FINAL CANDIDATE ASSESSMENT

==================================================
             FINAL EVALUATION
==================================================

Role: Python Developer
Skills: Python, SQL
Experience Level: Intermediate

Overall Score: 8.2/10

Strengths:
✓ Strong Python fundamentals
✓ Good SQL query optimization
✓ Clear problem-solving approach

Gaps:
✗ Limited system design depth
✗ Needs stronger error-handling practices

Recommendation:
Ready

Summary:
The candidate demonstrated strong Python and SQL fundamentals
with good practical problem-solving ability. Further improvement
in system design would strengthen their readiness for backend roles.

# ARCHITECTURE
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

# WHAT MAKES IT DIFFERENT

This is the section I'd definitely add for a challenge.

From a Question Generator → to an Evaluation Agent

The system isn't simply:

Prompt → LLM → Answer

Instead, it maintains an interview workflow:

Configure
   ↓
Generate Questions
   ↓
Collect Answer
   ↓
Evaluate
   ↓
Record Result
   ↓
Continue Interview
   ↓
Aggregate Performance
   ↓
Generate Candidate Assessment

This demonstrates:

LLM orchestration
Structured outputs
Stateful workflow
Tool/API integration
Evaluation
Persistent artifacts

Those are much stronger signals in an AI-agent challenge than simply calling an LLM.

# TECH STACK
| Layer             | Technology              |
| ----------------- | ----------------------- |
| Language          | Python                  |
| LLM Provider      | Groq                    |
| Model             | Llama 3.3 70B Versatile |
| Interface         | CLI                     |
| Configuration     | `.env`                  |
| Structured Output | JSON                    |
| Persistence       | JSON + Markdown         |
| Testing           | Mock mode               |

## 1 Install


```bash
git clone <this-repo-url>
cd interview_agent
python3 -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
```

Requires Python 3.9+.

## 2. Configure your Groq API key

1. Get a free key at https://console.groq.com/keys

   ```

## 3. Run it

### Interactive mode

Start the interview with:

```bash
python interview_agent.py.

# PROJECT STRUCTURE


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


### Offline mock mode (no API key / no network required)

To verify the agent's plumbing (question loop -> scoring -> final eval)
without calling any LLM at all, add `--mock`. This uses a simple local
heuristic instead of real language understanding — it's meant for testing
the code path, not for judging answer quality:

```bash
python interview_agent.py --role "Data Analyst" \
    --skills "SQL, Python, Statistics" --num-questions 5 \
    --answers-file sample_output/sample_answers.json --mock
```

Every run writes a timestamped transcript to `sessions/<timestamp>_<role>.json`
and `.md`.

### demo
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

Q1: How do you handle errors and exceptions in Python, and can you give an example of a try-except block you've used in a recent project?
Type your answer below.
Press ':submit' on a new line when you are finished.
> try block , place the code that might cause error inside this block
> except block , if error occurs in try block, python stops execting the remaining code there and jump directly to this block
> else, executes on;y if the code in try blovks runs perfectly 
> example is division by zero
> :submit
  -> Score: 6/10 | Feedback: The candidate provided a basic understanding of try-except blocks in Python, including the try, except, and else clauses, but the explanation was somewhat simplistic and lacked a concrete example from a recent project, and code syntax was not provided.

Q2: Describe a situation where you had to optimize the performance of a Python script, what steps did you take, and what were the results?
Type your answer below.
Press ':submit' on a new line when you are finished.
> i optimized a python script by first identying the slow part of the code, i reduced unnecassary loops, used built in functions and avoided repeated database quesries , after testing the changes the scrpit ran faster and used less memory
> :submit
  -> Score: 6/10 | Feedback: The candidate identified key steps to optimize a Python script, such as reducing unnecessary loops and using built-in functions, but the answer lacks specific details and metrics about the results, such as the percentage improvement in speed and memory usage.

Q3: Can you explain the difference between static typing and dynamic typing in programming languages, and how does Python's dynamic typing affect the way you design and write your code?
Type your answer below.
Press ':submit' on a new line when you are finished.
> static, that check before the program runs, while dynamic determined runtiime
> python is dynamically typed, so i do not need to declare the type of varible explicty, this makes python flexible
> :submit
  -> Score: 4/10 | Feedback: The candidate correctly identified Python as dynamically typed and mentioned the flexibility it provides, but the explanation of static and dynamic typing was brief and lacked clarity, and the answer could benefit from more specific examples and details on how dynamic typing affects code design.

Computing final evaluation...


==================================================
             FINAL EVALUATION
==================================================

Role: PYTHON
Skills: python
Experience Level: Intermediate

Overall Score: 5.33/10

Strengths:
✓ Basic understanding of try-except blocks
✓ Ability to identify key steps to optimize Python script performance

Gaps:
✗ Lack of concrete examples from recent projects
✗ Limited understanding of static and dynamic typing
✗ Need for improvement in code syntax and explanation clarity

Recommendation:
Needs Improvement


```
