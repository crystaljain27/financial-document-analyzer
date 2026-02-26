## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool:
    @tool("Read Financial Document")
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document file content
        """
        
        loader = PyPDFLoader(file_path=path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            # Clean and format the financial document data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report

## Creating Investment Analysis Tool
class InvestmentTool:
    @tool("Analyze Investment")
    def analyze_investment_tool(financial_document_data: str) -> str:
        """Analyze investment opportunities from financial document data.
        
        Args:
            financial_document_data (str): The financial document content to analyze.
            
        Returns:
            str: Investment analysis results.
        """
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format - remove double spaces
        while "  " in processed_data:
            processed_data = processed_data.replace("  ", " ")
                
        # Return processed data for further analysis by agents
        return processed_data

## Creating Risk Assessment Tool
class RiskTool:
    @tool("Create Risk Assessment")
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """Create risk assessment from financial document data.
        
        Args:
            financial_document_data (str): The financial document content to analyze.
            
        Returns:
            str: Risk assessment results.
        """
        # Process the data for risk assessment
        processed_data = financial_document_data
        
        # Return processed data for risk analysis by agents
        return processed_data