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
    > "Make it more technical"  
    > "...make it shorter"

- Overall status is `pass` only if all checks pass (i.e., no reasons collected); otherwise `fail`

## Evals



