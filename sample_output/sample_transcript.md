# Interview Transcript — Data Analyst

- **Skills probed:** SQL, Python, Statistics
- **Model:** llama-3.3-70b-versatile (Groq)
- **Timestamp (UTC):** 2026-08-14T12:00:00Z
- **Command used:**
  `python interview_agent.py --role "Data Analyst" --skills "SQL, Python, Statistics" --num-questions 5 --answers-file sample_output/sample_answers.json`

This transcript demonstrates the shape of a real run against the Groq API
(model: `llama-3.3-70b-versatile`). The reproducible, offline version of this
same run (using the local heuristic scorer instead of a live LLM) can be
regenerated at any time with:

```
python interview_agent.py --role "Data Analyst" --skills "SQL, Python, Statistics" \
    --num-questions 5 --mock --answers-file sample_output/sample_answers.json
```

## Questions & Answers

### Q1. Walk me through how you'd find the top 3 highest-paid employees in each department using SQL.
**Answer:** I'd start by writing a SQL query using window functions like RANK() partitioned by department to find the top earners, then join back to the employee table to pull names and titles.

**Score:** 8/10
**Feedback:** Correctly identifies RANK() with PARTITION BY as the right tool. Could have mentioned handling ties (RANK vs DENSE_RANK) or naming the exact join condition for full credit.

### Q2. What's the difference between normalized and denormalized database schemas, and when would you choose one over the other?
**Answer:** Normalization reduces data redundancy by splitting data into related tables, while denormalization combines tables back together to speed up read-heavy queries at the cost of some duplication. I'd denormalize for a reporting dashboard that's read far more than it's written.

**Score:** 9/10
**Feedback:** Clear, accurate definition with a concrete, well-reasoned use case. Strong answer.

### Q3. In Python, how would you compute total revenue per customer from a large CSV and rank customers by that total?
**Answer:** In Python I'd use pandas to load the CSV, then groupby the customer_id column and aggregate with sum() on the revenue column, followed by sort_values(ascending=False) to rank customers.

**Score:** 8/10
**Feedback:** Correct and idiomatic pandas approach. Could mention chunked reading for files too large to fit in memory.

### Q4. Tell me about a time you found and fixed a bug in a data pipeline or dashboard. What was your process?
**Answer:** Once, a dashboard I built was showing incorrect week-over-week numbers. I traced it to a timezone mismatch between the app server and the database, wrote a regression test, and documented the fix so it wouldn't recur.

**Score:** 9/10
**Feedback:** Excellent behavioral answer: clear root cause, a fix, a regression test, and documentation to prevent recurrence.

### Q5. How would you explain a p-value to a non-technical stakeholder, and what's a common misconception about it?
**Answer:** I'd explain a p-value as the probability of seeing data at least as extreme as what we observed, assuming the null hypothesis is true. A small p-value suggests the observed effect is unlikely to be due to chance alone, but it doesn't tell you the size or practical importance of the effect.

**Score:** 9/10
**Feedback:** Technically accurate definition and correctly flags the "statistical vs. practical significance" misconception. Strong communication for a non-technical audience.

## Final Evaluation

**Overall score:** 8.6/10

**Strengths:**
- Strong, idiomatic command of both SQL (window functions) and pandas for common analyst workflows.
- Statistical concepts (p-values) explained accurately and in stakeholder-friendly language.
- Debugging story shows a full root-cause -> fix -> regression-test -> documentation loop, not just a patch.

**Gaps:**
- Edge cases (tie-handling in ranking queries, out-of-memory data) were not proactively raised.
- No answer touched on experiment design or statistical power, which would round out the statistics skill area.

**Summary:** This candidate shows solid, practical SQL and Python skills for analyst work along with above-average statistical communication. Strong hire signal for a Data Analyst role; a follow-up round could probe experimental design and handling of messier, larger-scale data.
