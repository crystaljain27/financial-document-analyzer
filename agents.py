## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai import Agent
from langchain_openai import ChatOpenAI

from tools import search_tool, FinancialDocumentTool

### Loading LLM
llm = ChatOpenAI(
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate, data-driven financial analysis and investment insights based on the query: {query}. "
         "Analyze financial documents thoroughly to extract key metrics, trends, and performance indicators.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with 15+ years of experience in equity research and financial modeling. "
        "You have worked with major investment banks and have deep expertise in analyzing corporate financial statements, "
        "identifying market trends, and evaluating investment opportunities. You are known for your meticulous attention to detail "
        "and ability to uncover insights that others miss. You provide balanced, well-researched analysis that helps investors "
        "make informed decisions. You always base your recommendations on solid data and rigorous analysis."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify that uploaded documents are valid financial documents and extract key metadata. "
         "Ensure documents contain relevant financial information such as balance sheets, income statements, "
         "cash flow statements, or investment reports before processing.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous document verification specialist with expertise in financial reporting standards. "
        "You have worked in compliance and regulatory roles, ensuring that all financial documents meet required standards. "
        "You carefully examine each document to verify its authenticity, completeness, and relevance to financial analysis. "
        "Your attention to detail ensures that only valid financial documents proceed through the analysis pipeline."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=True
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide personalized investment recommendations based on thorough analysis of financial documents "
         "and the user's specific query: {query}. Consider risk tolerance, investment horizon, and market conditions.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial planner (CFP) and chartered financial analyst (CFA) with 15+ years of experience "
        "in wealth management and investment advisory. You have helped hundreds of clients build diversified portfolios "
        "tailored to their financial goals. You stay current with market trends, economic indicators, and investment strategies. "
        "You prioritize your clients' best interests and provide recommendations based on solid research and risk assessment. "
        "You are skilled at explaining complex investment concepts in clear, actionable terms."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Conduct comprehensive risk assessments of investments and financial strategies based on the query: {query}. "
         "Identify potential risks including market risk, credit risk, liquidity risk, and operational risk. "
         "Provide actionable risk mitigation strategies.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with expertise in quantitative risk analysis and portfolio risk assessment. "
        "You have worked with institutional investors and asset managers to identify, measure, and mitigate investment risks. "
        "You are proficient in risk modeling techniques including VaR (Value at Risk), stress testing, and scenario analysis. "
        "You provide balanced risk assessments that help investors understand potential downsides while identifying "
        "opportunities within their risk tolerance. Your recommendations are always grounded in rigorous analysis."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)
