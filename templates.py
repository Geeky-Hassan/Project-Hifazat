from pydantic import BaseModel, Field
from typing import Literal
from langchain.prompts import PromptTemplate

advisor_template = """You are Project Hifazat's legal research assistant, focused on helping 
women in Pakistan with their legal concerns. Using the provided vectorstore context, you must:

1. Analyze the query for specific legal issues in Pakistan's legal framework
2. Reference relevant laws, especially those protecting women's rights
3. Check for any emergency or safety concerns
4. Provide practical guidance considering cultural context
5. Include emergency helplines when needed
6. Offer guidance in both English and Urdu if requested
7. Direct to appropriate support services

Remember:
- Prioritize user safety
- Use clear, understandable language
- Include relevant emergency contacts
- Respect cultural sensitivities
- Maintain strict confidentiality

Context: {context}
Query: {query}

Always check for signs of emergency and include emergency contacts when safety is a concern."""

predictor_template = """As Project Hifazat's legal guide, analyze this legal situation based on:

1. Pakistani Women's Protection Laws
2. Similar case precedents in Pakistan
3. Available legal remedies and protections
4. Practical implementation challenges
5. Safety considerations

Key Focus Areas:
- Family Law implications
- Workplace harassment regulations
- Domestic violence protections
- Available support networks
- Immediate safety needs

Context: {context}
Query: {query}

Provide realistic analysis while prioritizing personal safety and practical solutions."""

example_generator_template = """
### Project Hifazat Legal Report
**Women's Rights and Legal Protection Analysis**

Context: {context}
Query: {query}

**Required Sections:**
1. **Title:**
   - Clear issue identification
   - Relevant legal category

2. **Situation Analysis:**
   - Legal rights under Pakistani law
   - Applicable protections
   - Safety considerations

3. **Legal Framework:**
   - Relevant Pakistani laws
   - Protection mechanisms
   - Implementation procedures

4. **Available Support:**
   - Legal aid services
   - Support organizations
   - Emergency contacts

5. **Practical Guidance:**
   - Immediate steps
   - Required documentation
   - Safety measures

6. **Recommendations:**
   - Short-term actions
   - Long-term considerations
   - Support resources

7. **Important Notice:**
   - AI assistance limitations
   - Professional legal consultation advice
   - Emergency services information

Ensure all guidance considers cultural context and safety priorities."""

generator_template = PromptTemplate.from_template(template=example_generator_template)

# Keep all the BaseModel classes exactly as they were
class LegalReportResponse(BaseModel):
    """Respond to the user with this"""
    return_direct: bool = False
    case_summary: str = Field(description="A concise summary of the legal case")
    relevant_precedents: str = Field(description="Key legal precedents or statutes relevant to the case")
    evidence_analysis: str = Field(description="Summary of evidence and arguments presented by both sides")
    key_findings: str = Field(description="Important findings or factors that influence the case")
    conclusion: str = Field(description="A brief conclusion based on the analysis")

class CaseOutcomePredictionResponse(BaseModel):
    """Respond to the user with this"""
    return_direct: bool = False
    outcome_prediction: str = Field(description="Predicted outcome of the case")
    confidence_interval: str = Field(description="Confidence interval for the prediction (e.g., 70% chance for the plaintiff)")
    jurisdiction: str = Field(description="The legal jurisdiction relevant to the prediction")
    uncertainty_factors: str = Field(description="Factors that might lead to different outcomes")
    disclaimer: str = Field(description="AI-generated prediction disclaimer for limitations")

class LegalAdviceResponse(BaseModel):
    """Respond to the user with this"""
    return_direct: bool = False
    legal_issue: str = Field(description="The specific legal issue or query addressed")
    advice: str = Field(description="The legal advice or recommendation provided based on the given context")
    relevant_sections: str = Field(description="Relevant sections from legal documents or case law supporting the advice")
    jurisdiction: str = Field(description="The jurisdiction applicable to the legal advice")
    conflicting_interpretations: str = Field(description="Any conflicting interpretations or unclear areas of law")
    next_steps: str = Field(description="Practical recommendations or next steps for the user to take")
    disclaimer: str = Field(description="AI-generated legal advice disclaimer for limitations")