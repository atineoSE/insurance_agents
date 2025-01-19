# Agentic workflow for a car insurance company with LangGraph and PGVector

## Intro
The following is an exercise in agentic workflow for a fictious car insurance company.

Main features:
- It uses LangGraph to orchestrate agents and LangChain to load helper components
- It leverages a vector store, in this case a PGVector store created with [Neon](https://neon.tech). A free account suffices for the purpose of validating the exercise.

## Setup
- Required dependencies are specified in Poetry. Existing requirements.txt file for pip has been removed to avoid confusion.
- We need to define 2 environment variables for the example to work:
* `NEON_CONNECTION_STRING`: to connect to the PGVector DB in Neon
* `OPENAI_API_KEY`: to get embeddings for document chunks and perform LLM inference

## Agentic workflow
- For the purpose of illustrating a multi-agent workflow or agent pipeline, we have created 3 different agents:
* `InsuranceAnalysisAgent`: it produces a market analysis from a user query, leveraging existing data in the provided documents under `iii.org`.
* `RiskAssessmentAgent`: it produces a risk analysis from a user query, leveraging internal model knowledge (one could easily imagine using a fine-tuned version for this agent or an additional vector store).
* `EarningsCallAgent`: it produces an earnings call report based on the market analysis and risk assessment data from upstream agents, plus information of previous earnings call (stored in memory for simplicity in this example).

Here is the agent graph:

![](./src/graph_chart.png)


The most important aspect of this diagram is the parallel nature of the `insurance_agent` and the `risk_assessment_agent`, and the recombination of both results before proceeding with the last step of the workflow with the `earnings_call_agent`.

This is representative of more complex flows, where agents have a dependency graph and need to be orchestrated accordingly. In this case, we use LangGraph for such orchestration.

## Assignments

The original assigments were:
* Task 1: Complete the Document Pipeline -> implemented in `DocumentProcessor`
* Task 2: Implement Vector Store -> implemented in `VectoStore`
* Task 3: Create Analysis Agent -> implemented in `InsuranceAnalysisAgent`

Additionally, new agents, additional dummy stores, and parallel flow have been implemented.

## Running the example

Run the example as follows:
1. Clone the repo
1. Set up the environment, using poetry (`poetry install; poetry shell`)
1. Create a DB in Neon.tech, copy the connection string and set it in the `.env` file.
1. Copy you OpenAI API key in the `.env` file.
1. Run the agent workflow as follows.

`cd src; python main.py --debug --query "<your_natural_language_query_over_car_insurance>" --docs-dir ../iii.org`

The first time the script runs, the documents are chunked and stored in the PGVector DB. This is only done once.

You can find sample outputs in the `output` directory.

## Sample output

Here is one output sample for convenience:

**Query: What's the trend in auto insurance costs over the last 3 years?**

**Answer:**
## Earnings Call Report: AutoGuard Insurance Inc.

### Market Analysis:
The trend in auto insurance costs over the last 3 years for AutoGuard Insurance Inc. is as follows:
- In 2011, the average expenditure was $797.
- In 2012, the average expenditure increased to $814.63, showing a 2.1% increase.
- In 2013, the average expenditure further increased to $841.23, indicating a 3.3% rise.

The trend in auto insurance costs over the last 3 years has been increasing, reflecting the industry's upward trajectory in premium rates.

### Risk Assessment:
When assessing the trend in auto insurance costs over the last 3 years, AutoGuard Insurance Inc. considers several risks:
1. **Market Trends**: Fluctuations in the economy impacting insurance costs.
2. **Regulatory Changes**: Impact of new laws and regulations on insurance costs.
3. **Technological Advancements**: Increasing repair costs due to advanced vehicle technologies.
4. **Natural Disasters**: Surge in insurance claims from disasters affecting premiums.
5. **Driving Habits**: Changes in habits leading to more accidents and costs.
6. **Competition**: Price wars affecting overall insurance costs.
7. **Claims Frequency and Severity**: Higher costs from increased claims.

By addressing these risks, AutoGuard Insurance Inc. can make informed decisions to manage pricing strategies, underwriting practices, and risk mitigation techniques effectively.

### Financial Performance:
- **Q3 2024**: Net income of $180 million, revenue of $1.4 billion, with a combined ratio of 93.5%.
- **Q4 2024**: Net income increased to $200 million, revenue rose to $1.6 billion, with a combined ratio of 92.2%.
- **Strategic Initiatives**: Progress in digital transformation, data analytics, and market expansion.

### Future Outlook:
- Full-year 2024 net income expected to be $720-$780 million.
- Full-year 2024 revenue forecasted to be $5.6-$6.0 billion.
- Strong positioning for 2025 with expected net income of $800-$850 million and revenue of $6.2-$6.7 billion.

