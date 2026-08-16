#!/usr/bin/env python3
"""
Interview Agent
================
A CLI AI agent that conducts a structured mock interview:
  1. Generates role-specific interview questions (via Groq LLM).
  2. Accepts candidate answers (typed, or supplied from a file for
     non-interactive / reproducible runs).
  3. Scores each answer (1-10) with brief feedback.
  4. Produces a final evaluation: overall score, strengths, gaps.
  5. Saves a full transcript (JSON + Markdown) to ./sessions/.

Usage
-----
Interactive (real LLM calls via Groq):
    export GROQ_API_KEY="your_key_here"
    python interview_agent.py --role "Backend Engineer" \
        --skills "Python, SQL, System Design" --num-questions 5

Non-interactive / reproducible demo (answers piped from a file, still
uses the real Groq API if a key is set):
    python interview_agent.py --role "Data Analyst" \
        --skills "SQL, Python, Statistics" \
        --answers-file sample_output/sample_answers.json

Offline mock mode (no API key / no network needed -- useful for
grading the plumbing of the agent without an LLM key):
    python interview_agent.py --role "Data Analyst" \
        --skills "SQL, Python" --mock \
        --answers-file sample_output/sample_answers.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------------
# LLM CLIENT (Groq)
# ----------------------------------------------------------------------
# We isolate all model access behind a tiny interface (`chat`) so the
# rest of the agent doesn't care whether it's hitting Groq or running
# in --mock mode.

DEFAULT_MODEL = "llama-3.3-70b-versatile"


class LLMClient:
    """Thin wrapper around the Groq chat-completions API."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Export it or put it in a .env file "
                "(see .env.example). Or pass --mock to run without an LLM."
            )
        try:
            from groq import Groq
        except ImportError as e:
            raise RuntimeError(
                "The 'groq' package is not installed. Run: pip install -r requirements.txt"
            ) from e
        self._client = Groq(api_key=api_key)

    def chat(self, system: str, user: str, temperature: float = 0.4) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content


class MockLLMClient:
    """
    Deterministic, offline stand-in for LLMClient.

    Lets a reviewer run the full agent loop (question generation ->
    scoring -> final evaluation) with zero network access and zero API
    key, purely to verify the *plumbing* of the agent. Real language
    understanding requires --mock to be OFF (i.e. a real Groq key).
    """

    def __init__(self, model: str = "mock-local"):
        self.model = model

    def chat(self, system: str, user: str, temperature: float = 0.4) -> str:
        sys_l = system.lower()
        # Order matters: check the most specific prompt first, since
        # "final evaluation" prompts also contain the substring "score"
        # (e.g. "overall_score") which would otherwise false-match.
        if "final evaluation" in sys_l:
            return self._mock_final(user)
        if "generate" in sys_l and "question" in sys_l:
            return self._mock_questions(user)
        if "scoring" in sys_l:
            return self._mock_score(user)
        return "{}"

    @staticmethod
    def _mock_questions(user: str) -> str:
        m = re.search(r"Number of questions:\s*(\d+)", user)
        n = int(m.group(1)) if m else 5
        role_m = re.search(r"Role:\s*(.+)", user)
        role = role_m.group(1).strip() if role_m else "the role"
        qs = [
            f"Tell me about a project where you applied skills relevant to {role}."
            if i == 0 else f"Mock question #{i+1} relevant to {role} (offline placeholder)."
            for i in range(n)
        ]
        return json.dumps({"questions": qs})

    @staticmethod
    def _mock_score(user: str) -> str:
        ans_m = re.search(r"Candidate answer:\s*(.*)", user, re.DOTALL)
        answer = ans_m.group(1).strip() if ans_m else ""
        length = len(answer.split())
        score = max(1, min(10, 3 + length // 8))
        return json.dumps({
            "score": score,
            "feedback": f"(mock) Answer had {length} words; heuristic length-based score."
        })

    @staticmethod
    @staticmethod
    def _mock_final(user: str) -> str:
        scores = [int(s) for s in re.findall(r'"score":\s*(\d+)', user)]
        avg = round(sum(scores) / len(scores), 1) if scores else 0

        if avg >= 9.0:
            recommendation = "Strong Hire"
        elif avg >= 8.0:
            recommendation = "Hire"
        elif avg >= 7.0:
            recommendation = "Consider"
        elif avg >= 6.0:
            recommendation = "Weak Consider"
        else:
            recommendation = "Needs Improvement"

        return json.dumps({
            "overall_score": avg,
            "strengths": [
                "(mock) Answered every question",
                "(mock) Reasonable detail length"
            ],
            "gaps": [
                "(mock) No real semantic evaluation was performed offline"
            ],
            "recommendation": recommendation,
            "summary": f"(mock) Candidate averaged {avg}/10 across all questions."
        })


# ----------------------------------------------------------------------
# JSON EXTRACTION HELPER
# ----------------------------------------------------------------------

def extract_json(text: str) -> dict:
    """LLMs sometimes wrap JSON in prose or code fences. Pull the JSON out."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    else:
        brace = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if brace:
            text = brace.group(1)
    return json.loads(text)


# ----------------------------------------------------------------------
# AGENT LOGIC
# ----------------------------------------------------------------------

QUESTION_SYSTEM_PROMPT = """You are an expert technical interviewer. \
Generate role-specific interview questions.
Rules:
- Return ONLY valid JSON, no prose, no markdown fences.
- JSON shape: {"questions": ["...", "...", ...]}
- Mix conceptual, situational/behavioral, and applied/technical questions.
- Questions must be relevant to the given role and skills.
- Do not number the questions inside the text.
"""

SCORE_SYSTEM_PROMPT = """You are an expert interviewer scoring a candidate's answer.
Rules:
- Return ONLY valid JSON, no prose, no markdown fences.
- JSON shape: {"score": <integer 1-10>, "feedback": "<1-3 sentence feedback>"}
- Score 1-3 = poor/incorrect, 4-6 = partial/adequate, 7-8 = strong, 9-10 = excellent/expert.
- Judge accuracy, depth, and relevance to the question and role.
- Be concise and specific in feedback (mention what was good or missing).
"""

FINAL_EVAL_SYSTEM_PROMPT = """You are an expert interviewer writing a final evaluation summary.
This is the final evaluation for the interview.

Rules:
- Return ONLY valid JSON, no prose, no markdown fences.
- JSON shape:
{
  "overall_score": <float 1-10>,
  "strengths": ["...", "..."],
  "gaps": ["...", "..."],
  "recommendation": "<Strong Hire / Hire / Consider / Weak Consider / Needs Improvement>",  "summary": "<2-4 sentence overall summary>"
}
- Base the overall_score primarily on the per-question scores provided.
- Consider the candidate's experience level when making the recommendation.
- Be fair and specific.
- Recommendation thresholds:
  - 9.0-10.0 = Strong Hire
  - 8.0-8.9 = Hire
  - 7.0-7.9 = Consider
  - 6.0-6.9 = Weak Consider
  - Below 6.0 = Needs Improvement
"""


class InterviewAgent:
    def __init__(
        self,
        llm,
        role: str,
        skills: str,
        experience_level: str,
        num_questions: int = 5
    ):
        self.llm = llm
        self.role = role
        self.skills = skills
        self.experience_level = experience_level
        self.num_questions = num_questions
        self.transcript = []  # list of {question, answer, score, feedback}

    def generate_questions(self) -> list:
        user_prompt = (
            f"Role: {self.role}\n"
            f"Key skills to probe: {self.skills}\n"
            f"Experience level: {self.experience_level}\n"
            f"Number of questions: {self.num_questions}\n"
             "Generate questions appropriate for the candidate's experience level.\n"
            "Generate the questions now."
        )
        raw = self.llm.chat(QUESTION_SYSTEM_PROMPT, user_prompt)
        try:
            data = extract_json(raw)
            questions = data["questions"]
        except Exception:
            # Fallback: split raw text into lines if JSON parsing fails
            questions = [
                l.strip("-• \t") for l in raw.splitlines() if l.strip()
            ][: self.num_questions]
        return questions[: self.num_questions]

    def score_answer(self, question: str, answer: str) -> dict:
        user_prompt = (
            f"Role: {self.role}\n"
            f"Question: {question}\n"
            f"Candidate answer: {answer}\n"
            "Score this answer now."
        )
        raw = self.llm.chat(SCORE_SYSTEM_PROMPT, user_prompt)
        try:
            data = extract_json(raw)
            score = int(data.get("score", 0))
            feedback = str(data.get("feedback", "")).strip()
        except Exception:
            score, feedback = 0, f"(unparsed model output) {raw[:200]}"
        return {"score": score, "feedback": feedback}

    def record(self, question: str, answer: str, score: int, feedback: str):
        self.transcript.append({
            "question": question,
            "answer": answer,
            "score": score,
            "feedback": feedback,
        })

    def final_evaluation(self) -> dict:
        user_prompt = (
            f"Role: {self.role}\n"
            f"Skills probed: {self.skills}\n"
            f"Per-question results (JSON): {json.dumps(self.transcript)}\n"
            "Write the final evaluation now."
        )
        raw = self.llm.chat(FINAL_EVAL_SYSTEM_PROMPT, user_prompt)
        try:
            return extract_json(raw)
        except Exception:
            scores = [t["score"] for t in self.transcript if t["score"]]
            avg = round(sum(scores) / len(scores), 1) if scores else 0
            return {
                "overall_score": avg,
                "strengths": [],
                "gaps": [],
                "summary": f"(fallback, model output unparsable) Average score: {avg}/10.",
            }


# ----------------------------------------------------------------------
# I/O HELPERS
# ----------------------------------------------------------------------

def get_answer(question: str, idx: int, canned_answers, interactive: bool) -> str:
    if canned_answers is not None:
        if idx < len(canned_answers):
            answer = canned_answers[idx]
            print(f"\nQ{idx + 1}: {question}")
            print(f"(from answers file) A{idx + 1}: {answer}")
            return answer
        return ""  # ran out of canned answers
    if not interactive:
        raise RuntimeError(
            "No --answers-file provided and stdin is not interactive. "
            "Provide --answers-file or run in a real terminal."
        )
    print(f"\nQ{idx + 1}: {question}")
    print("Type your answer below.")
    print("Press ':submit' on a new line when you are finished.")

    lines = []

    while True:
        line = input("> ")

        if line.strip() == ":submit":
            break

        lines.append(line)

    return "\n".join(lines).strip()
    


def save_transcript(session: dict, out_dir: Path) -> tuple:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    role_slug = re.sub(r"[^a-zA-Z0-9]+", "-", session["role"]).strip("-").lower()
    base = out_dir / f"{ts}_{role_slug}"

    json_path = base.with_suffix(".json")
    json_path.write_text(json.dumps(session, indent=2), encoding="utf-8")

    md_lines = [
        f"# Interview Transcript — {session['role']}",
        "",
        f"- **Skills probed:** {session['skills']}",
         f"- **Experience level:** {session.get('experience_level', 'N/A')}",
        f"- **Model:** {session['model']}",
        f"- **Timestamp (UTC):** {session['timestamp']}",
        "",
        "## Questions & Answers",
        "",
    ]
    for i, t in enumerate(session["transcript"], 1):
        md_lines += [
            f"### Q{i}. {t['question']}",
            f"**Answer:** {t['answer']}",
            "",
            f"**Score:** {t['score']}/10",
            f"**Feedback:** {t['feedback']}",
            "",
        ]
    fe = session["final_evaluation"]
    md_lines += [
        "## Final Evaluation",
        "",
        f"**Overall score:** {fe.get('overall_score', 'N/A')}/10",
        "",
        "**Strengths:**",
    ] + [f"- {s}" for s in fe.get("strengths", [])] + [
        "",
        "**Gaps:**",
    ] + [f"- {g}" for g in fe.get("gaps", [])] + [
        "",
        f"**Summary:** {fe.get('summary', '')}",
        "",
    ]
    md_path = base.with_suffix(".md")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    return json_path, md_path

def get_interview_setup():
    print("\n" + "=" * 50)
    print("           AI INTERVIEW AGENT")
    print("=" * 50)

    role = input("\nEnter your role: ").strip()

    while not role:
        print("Role cannot be empty.")
        role = input("Enter your role: ").strip()

    skills = input("Enter your skills (comma separated): ").strip()

    while not skills:
        print("Skills cannot be empty.")
        skills = input("Enter your skills: ").strip()

    print("\nSelect your experience level:")
    print("1. Fresher")
    print("2. Intermediate")
    print("3. Advanced")

    while True:
        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            experience_level = "Fresher"
            break
        elif choice == "2":
            experience_level = "Intermediate"
            break
        elif choice == "3":
            experience_level = "Advanced"
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    while True:
        num_input = input("\nHow many questions? [default: 5]: ").strip()

        if num_input == "":
            num_questions = 5
            break

        if num_input.isdigit() and int(num_input) > 0:
            num_questions = int(num_input)
            break

        print("Please enter a valid positive number.")

    print("\n" + "-" * 50)
    print("INTERVIEW CONFIGURATION")
    print("-" * 50)
    print(f"Role             : {role}")
    print(f"Skills           : {skills}")
    print(f"Experience Level : {experience_level}")
    print(f"Questions        : {num_questions}")
    print("-" * 50)

    confirm = input("\nStart interview? (y/n): ").strip().lower()

    if confirm not in ("y", "yes"):
        print("Interview cancelled.")
        sys.exit(0)

    return role, skills, experience_level, num_questions

# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI Interview Agent (Groq-powered)")
    parser.add_argument("--role", help='e.g. "Backend Engineer"')
    parser.add_argument("--skills", help='e.g. "Python, SQL, System Design"')
    parser.add_argument("--num-questions", type=int, default=5)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model name")
    parser.add_argument(
        "--answers-file",
        help="JSON file with a list of answer strings, for non-interactive runs. "
             'e.g. ["My answer to Q1", "My answer to Q2", ...]',
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run fully offline with a local heuristic instead of calling Groq. "
             "Useful for testing the agent loop without an API key.",
    )
    parser.add_argument(
        "--out-dir", default="sessions", help="Where to save transcript files"
    )
    args = parser.parse_args()
    if args.role is None and args.skills is None:
            role, skills, experience_level, num_questions = get_interview_setup()
    else:
        role = args.role
        skills = args.skills
        experience_level = "Intermediate"
        num_questions = args.num_questions
   
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    canned_answers = None
    if args.answers_file:
        canned_answers = json.loads(Path(args.answers_file).read_text(encoding="utf-8"))

    if args.mock:
        llm = MockLLMClient()
    else:
        try:
            llm = LLMClient(model=args.model)
        except RuntimeError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)

    agent = InterviewAgent(llm, role=role, skills=skills,experience_level=experience_level,
                            num_questions=num_questions)

    print(
    f"\n=== Interview Agent === "
    f"role={role!r} "
    f"skills={skills!r} "
    f"level={experience_level!r} "
    f"n={num_questions} "
    f"mode={'mock' if args.mock else args.model}"
    )
    print("Generating questions...")
    questions = agent.generate_questions()
    if len(questions) < num_questions:
        print(f"[WARN] Model returned only {len(questions)} question(s).")

    interactive = sys.stdin.isatty()
    for i, q in enumerate(questions):
        answer = get_answer(q, i, canned_answers, interactive)
        result = agent.score_answer(q, answer)
        agent.record(q, answer, result["score"], result["feedback"])
        print(f"  -> Score: {result['score']}/10 | Feedback: {result['feedback']}")

    print("\nComputing final evaluation...")
    final_eval = agent.final_evaluation()

    session = {
        "role": role,
        "skills":skills,
        "experince_level":experience_level,
        "model": "mock-local" if args.mock else args.model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transcript": agent.transcript,
        "final_evaluation": final_eval,
    }

    json_path, md_path = save_transcript(session, Path(args.out_dir))

    print("\n")
    print("=" * 50)
    print("             FINAL EVALUATION")
    print("=" * 50)

    print(f"\nRole: {role}")
    print(f"Skills: {skills}")
    print(f"Experience Level: {experience_level}")

    print(f"\nOverall Score: {final_eval.get('overall_score', 'N/A')}/10")

    print("\nStrengths:")
    for strength in final_eval.get("strengths", []):
        print(f"✓ {strength}")

    print("\nGaps:")
    for gap in final_eval.get("gaps", []):
        print(f"✗ {gap}")

    print("\nRecommendation:")
    print(final_eval.get("recommendation", "Needs Improvement"))

    print(f"\nSaved transcript to:")
    print(f"  {json_path}")
    print(f"  {md_path}")

if __name__ == "__main__":
    main()
