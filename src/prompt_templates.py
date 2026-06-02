"""Prompt templates for various financial and accounting tasks."""

ACCOUNTING_ANALYSIS_PROMPT = """
You are an expert financial accountant. Analyze the following accounting data and provide insights.

Context:
- Company: Generic finance and operations business
- Data period: {period}
- Total entries: {total_entries}

Data summary:
{data_summary}

Question: {question}

Please provide:
1. Clear answer to the question
2. Key findings from the data
3. Recommendations if applicable

Use specific numbers and percentages from the data.
"""

GENERAL_FINANCE_QUESTION_PROMPT = """
Tu es un expert en finance, comptabilité et contrôle de gestion.

Références documentaires disponibles:
{context}

Question utilisateur: {question}

Consignes:
- Réponds exclusivement en français
- Cite les sources documentaires utilisées
- Si l'information n'est pas disponible, dis-le clairement
- Utilise le contexte métier disponible dans la documentation
- Donne une réponse concise et directement utile

Réponse:
"""

MANAGEMENT_COMMENTARY_PROMPT = """
You are a financial director preparing a management comment for the executive committee.

Financial summary:
{financial_data}

Budget analysis:
{budget_analysis}

Issues and risks:
{issues}

Please write a professional management comment (200-300 words) that:
1. Summarizes the financial performance
2. Highlights key variances
3. Identifies risks and opportunities
4. Makes recommendations

Format: Professional memo to the CFO
"""

BUDGET_ANALYSIS_PROMPT = """
Analyze the budget vs actual variances for this cost center:

{budget_data}

Identify:
1. Top 3 positive variances (under budget)
2. Top 3 negative variances (over budget)
3. Trends and patterns
4. Recommendations for management

Format: Clear, concise report for management review.
"""

QUALITY_CHECK_PROMPT = """
Review data quality issues and prioritize them:

{issues_summary}

For each issue category:
1. Count and percentage of total data
2. Business impact
3. Recommended action
4. Timeline for resolution

Format: Priority-ordered action list.
"""

RAG_SYSTEM_PROMPT = """
Tu es un assistant IA financier spécialisé en:
- Comptabilité et saisie
- Trésorerie
- Contrôle de gestion
- Analyse budgétaire
- Reporting financier
- Finance et opérations

Tu as accès à des procédures et guides internes.
Réponds toujours en français.
Cite tes sources quand tu réponds.
Si l'information pertinente est absente, dis-le explicitement.
"""

SUPPLIER_ANALYSIS_PROMPT = """
Analyze the supplier and accounts payable situation:

{supplier_data}

Provide:
1. Top 10 suppliers by amount
2. Payment performance analysis
3. Overdue invoices status
4. Recommendations for cash management

Format: Executive summary with supporting tables.
"""

TREASURY_ANALYSIS_PROMPT = """
Analyze the company's treasury position:

{treasury_data}

Assess:
1. Cash flow trends
2. Liquidity position
3. Bank reconciliation status
4. Forecast for next 30 days

Format: Treasury report for CFO review.
"""

ANOMALY_DETECTION_PROMPT = """
You identified several accounting anomalies. Explain them:

Anomalies:
{anomalies}

For each anomaly:
1. What is wrong
2. Potential causes
3. Severity (low/medium/high)
4. Recommended action

Format: Risk assessment report.
"""
