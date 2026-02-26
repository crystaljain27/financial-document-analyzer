## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="""Analyze the financial document thoroughly to answer the user's query: {query}

Follow these steps:
1. Read the financial document using the available tool
2. Extract key financial metrics (revenue, profit margins, cash flow, etc.)
3. Identify trends and patterns in the financial data
4. Compare performance against industry benchmarks if possible
5. Provide a comprehensive analysis addressing the user's specific query

Focus on:
- Revenue growth and profitability trends
- Balance sheet strength
- Cash flow generation
- Key business segment performance
- Management's forward-looking statements
- Any risks or challenges mentioned

Use the financial document tool to read the file and search tool for additional market context if needed.""",

    expected_output="""A comprehensive financial analysis report that includes:
1. Executive Summary - Key findings and highlights
2. Financial Performance Analysis:
   - Revenue and earnings trends
   - Profitability metrics (gross margin, operating margin, net margin)
   - Cash flow analysis
3. Balance Sheet Strength:
   - Assets, liabilities, and equity position
   - Debt levels and liquidity
4. Key Insights - Important observations from the document
5. Conclusion - Summary addressing the user's query

The response should be professional, data-driven, and directly relevant to the user's query.""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""Provide investment recommendations based on the financial document analysis.
User query: {query}

Follow these steps:
1. Read and analyze the financial document thoroughly
2. Evaluate the company's financial health and growth prospects
3. Assess valuation metrics (P/E ratio, P/B ratio, EV/EBITDA, etc.)
4. Consider industry trends and competitive positioning
5. Analyze management's strategy and execution
6. Provide clear buy/hold/sell recommendations with rationale

Consider:
- Growth potential and market opportunities
- Competitive advantages and moats
- Valuation relative to peers and historical averages
- Dividend policy and shareholder returns
- Risk factors that could impact investment thesis""",

    expected_output="""A comprehensive investment recommendation report that includes:
1. Investment Thesis - Summary of the investment opportunity
2. Valuation Analysis:
   - Current valuation metrics
   - Comparison with industry peers
   - Historical valuation trends
3. Growth Catalysts - Key drivers for future growth
4. Risk Factors - Potential challenges and downside risks
5. Recommendation:
   - Clear buy/hold/sell rating
   - Target price range if applicable
   - Investment time horizon
   - Position sizing guidance
6. Supporting Data - Key financial metrics backing the recommendation""",

    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="""Conduct a comprehensive risk assessment of the investment based on the financial document.
User query: {query}

Follow these steps:
1. Read the financial document carefully
2. Identify and categorize different types of risks:
   - Market risk (interest rates, currency, commodity prices)
   - Credit risk (counterparty exposure, debt quality)
   - Liquidity risk (cash flow, working capital)
   - Operational risk (supply chain, execution)
   - Regulatory and compliance risk
   - Strategic risk (competition, technology disruption)
3. Assess the magnitude and probability of each risk
4. Evaluate the company's risk management practices
5. Provide risk mitigation recommendations

Consider:
- Financial leverage and debt servicing capability
- Revenue concentration and customer diversification
- Geographic and currency exposure
- Industry-specific risks
- Macroeconomic factors affecting the business""",

    expected_output="""A comprehensive risk assessment report that includes:
1. Risk Summary - Overview of key risk factors identified
2. Detailed Risk Analysis:
   - Market Risks: Interest rate sensitivity, currency exposure, commodity risks
   - Credit Risks: Debt levels, credit ratings, counterparty risks
   - Liquidity Risks: Cash flow adequacy, working capital needs
   - Operational Risks: Supply chain, key person dependencies
   - Strategic Risks: Competitive threats, technology disruption
3. Risk Ratings:
   - Overall risk rating (Low/Medium/High)
   - Individual risk category ratings
4. Risk Mitigation Strategies:
   - Recommended hedging strategies
   - Diversification suggestions
   - Monitoring indicators
5. Risk-Adjusted Investment Considerations - How risks affect the investment thesis""",

    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

    
verification = Task(
    description="""Verify that the uploaded document is a valid financial document.

Follow these steps:
1. Read the document using the available tool
2. Check for presence of financial content:
   - Financial statements (balance sheet, income statement, cash flow)
   - Financial metrics and ratios
   - Business performance data
   - Investment-related information
   - Auditor information (for official reports)
3. Verify document structure and formatting
4. Extract key metadata (company name, reporting period, document type)
5. Confirm the document is suitable for financial analysis

If the document is not a valid financial document, clearly state why and what type of document it appears to be.""",

    expected_output="""A verification report that includes:
1. Document Validity - Whether the document is a valid financial document (Yes/No)
2. Document Type - Type of financial document (10-K, 10-Q, Earnings Report, etc.)
3. Company Information:
   - Company name
   - Reporting period
   - Fiscal year/quarter
4. Content Summary - Key financial sections identified
5. Verification Status - Confirmed elements and any concerns
6. Recommendation - Whether the document should proceed to analysis""",

    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)