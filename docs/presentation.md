# AI Content Marketing Assistant

## Project Overview

- Key Features
- Architecture
- Approach
    - Plan Files
    - Iterative loop with Open AI
    - Incremental Steps
    - Tests green each step
- Streamlit UI

## Example

```JSON
{
  "topic": "blogging about bringing modern AI and ML to Hartsfield Jackson International Airport, the busiest airport in the world",
  "audience": "data scientists and AI engineers",
  "intent": "create|revise"
}
```
- *Router agent:* `create` routes through research -> strategist; but `revise` skips research, goes directly to rewrite  
    > Make it more technical  
    > Level of technicality is good, but make it shorter

- Overall status is `pass` only if all checks pass (i.e., no reasons collected); otherwise `fail`

## Evals

### Create Golden Set

- Each *golden case* uses **YAML**: structured test data that eval harness reads and turns into a controlled scenario
- Intentionally set up a known condition (not random cases) and check whether the full system responds the way you want.
- File is saying:
    > Run the system on a LinkedIn content-generation task about AI content governance for B2B teams, but instead of letting every node behave freely, inject very specific research inputs and a very specific writer output, then check whether the system handles that situation correctly.
- Addresses the question:
    > Can the pipeline recover from a specific class of writer defect?

### Defining a golden case:

1. Identify a failure mode you want to stress
2. Design a deterministic fixture that forces that failure
3. Define expectations that prove the system handled it correctly
4. Write the YAML in the exact structure your harness expects

### Kinds of golden cases

0. Baseline pass-through (Happy Path) (case #1)

    - Clean `create` flow that should pass without rewrite
    - Need this because a system that rewrites "everything" is often over-correcting or inefficient

1. Preventative guardrail case (case #2)

    - Inject mixed citations (valid + invalid) into writer output.
    - Verify deterministic post-processing removes out-of-research citations before quality evaluation.
    - Confirm citation integrity metrics pass (citation_subset / precision behavior) without requiring a revise loop.

2. Detection / routing case (case 6)

    Prove:

    - the bad draft is recognized as bad
    - the system chooses revise

    Expections:

    - expected_route: revise
    - min_rewrite_count: 1

3. Full recovery case (better eval, cases 3-5*, 7-9)

    Prove:

    - the initial draft is bad
    - the system routes to revise
    - the revised draft is actually better
    - the final result passes quality

    First draft:

    > AI governance is the ultimate game changer!  Sign up today!

    Quality checker must produce failure signals:

    - tone too promotional
    - not appropriate for B2B LinkedIn thought leadership
    - CTA too aggressive

    Revise step:

    > Rewrite this post for enterprise marketing leaders in a calm, analytical tone. Remove exaggerated sales language. Preserve the core topic and citations. End with a soft CTA suitable for LinkedIn.

    Then the rewritten version might become:

    > AI governance helps B2B teams make generated content more reusable, reviewable, and trustworthy.  Teams with documented review workflows reduce quality drift and improve consistency.  Worth asking: where does governance sit in your current content process?

### Using Golden Cases - Ideal workflow

1. Isolate a failing or weak case and run that case repeatedly
2. Iterate locally by adjusting prompts, quality rules, rewrite instructions, etc.
3. Run the full suite and confirm no regressions
4. Commit if metrics improved (golden metrics become acceptance gate)

### Towards Production

- Add full recovery tests with live LLM calls to explore broader (non-deterministic) behavior
- Add challenge cases:

    - Harder edge cases designed to expose weakness
    - Some are expected to fail (to prove detection/guardrails work)
    - Some are expected to pass to prove robustness under hard input

- Add agents to add images and other pathways, e.g., blog