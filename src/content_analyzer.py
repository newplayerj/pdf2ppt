import logging
from typing import Dict, Any
import openai
import json
import os

logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self):
        """Initialize content analyzer with OpenAI client."""
        self.client = openai.OpenAI()
        
    def _clean_json_response(self, response: str) -> str:
        """Clean the JSON response by removing markdown code blocks and other formatting."""
        # Remove markdown code blocks
        cleaned = response.replace('```json', '').replace('```', '')
        # Strip whitespace
        cleaned = cleaned.strip()
        logger.debug(f"Original response: {response}")
        logger.debug(f"Cleaned response: {cleaned}")
        return cleaned
        
    def analyze_content(self, text_content: str) -> Dict[str, Any]:
        """Analyze content with integrated section and figure analysis."""
        try:
            # Step 1: Extract paper structure
            structure_prompt = f"""
            Analyze this academic paper and extract its exact structure.
            Return ONLY the JSON structure with the following format:
            {{
                "title": "paper title",
                "sections": [
                    {{
                        "title": "section title",
                        "content": [
                            {{
                                "subtitle": "subsection title",
                                "points": ["point 1", "point 2"],
                                "figures": ["Figure X"]
                            }}
                        ]
                    }}
                ]
            }}
            
            Paper text:
            {text_content}
            """

            structure_response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a JSON generator. Return only valid JSON without any markdown formatting or additional text."
                    },
                    {"role": "user", "content": structure_prompt}
                ],
                temperature=0.1
            )
            
            # Get the response content and clean it
            raw_structure = structure_response.choices[0].message.content
            cleaned_structure = self._clean_json_response(raw_structure)
            
            try:
                paper_structure = json.loads(cleaned_structure)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse structure JSON: {e}")
                logger.error(f"Raw response: {raw_structure}")
                logger.error(f"Cleaned response: {cleaned_structure}")
                raise
            
            # Step 2: Enhanced content analysis with integrated figure context
            content_prompt = f"""
            Perform a comprehensive analysis of this academic paper. For each section:

            1. Section Overview:
               - Main objective of the section
               - Key concepts introduced
               - Connection to overall paper narrative
               - Critical findings or arguments

            2. Detailed Content Analysis:
               For each paragraph/subsection:
               - Core argument or finding with specific numbers
               - Supporting evidence and citations
               - Technical details and methodology
               - Connection to previous points
               - Impact on subsequent arguments

            3. Integrated Figure Analysis:
               When analyzing figures in context:
               - How the figure supports the current argument
               - Specific data or results shown
               - Technical details illustrated
               - Connection to surrounding text
               - Impact on conclusions

            4. Technical Flow:
               - Methodological progression
               - Result dependencies
               - Logical connections between sections
               - Build-up of arguments
               - Validation of claims

            Return the analysis in this JSON format:
            {{
                "title": "paper title",
                "sections": [
                    {{
                        "title": "section title",
                        "overview": "section's main points and role",
                        "content": [
                            {{
                                "subtitle": "logical subsection title",
                                "key_points": [
                                    {{
                                        "argument": "main argument or finding",
                                        "evidence": "supporting evidence with numbers",
                                        "technical_details": "methodology or implementation",
                                        "implications": "impact on overall narrative"
                                    }}
                                ],
                                "figures": [
                                    {{
                                        "reference": "Figure X",
                                        "description": "comprehensive description",
                                        "technical_content": "methods and approach shown",
                                        "results": "specific findings and measurements",
                                        "integration": "how it supports the argument",
                                        "panel_details": ["panel a details", "panel b details"]
                                    }}
                                ]
                            }}
                        ]
                    }}
                ]
            }}

            Guidelines for Analysis:
            1. Maintain paper's logical flow
            2. Include all quantitative details
            3. Preserve technical accuracy
            4. Show connections between sections
            5. Integrate figures with main text
            6. Highlight critical findings
            7. Explain methodological choices

            Paper structure:
            {json.dumps(paper_structure, indent=2)}

            Paper text:
            {text_content}
            """

            content_response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an expert academic paper analyzer with deep technical knowledge. 
                        Create a comprehensive analysis that maintains the paper's logical flow while integrating 
                        detailed technical content, quantitative results, and figure descriptions. Focus on accuracy 
                        and completeness."""
                    },
                    {"role": "user", "content": content_prompt}
                ],
                temperature=0.2,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )

            # Parse and return the content
            return json.loads(content_response.choices[0].message.content)

        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            raise

    def _extract_figure_context(self, text_content: str, figure_ref: str) -> Dict[str, Any]:
        """
        Extract comprehensive context for a figure by combining multiple sources of information.
        Returns a structured dictionary with detailed figure information.
        """
        try:
            context_prompt = f"""
            Analyze {figure_ref} comprehensively using the following text. 
            Provide a structured analysis including:

            1. Caption and Basic Information:
               - Full figure caption
               - Figure type (graph, diagram, flowchart, etc.)
               - Number of panels and their labels

            2. Technical Content:
               - Methodology or approach illustrated
               - Key components and their relationships
               - Technical parameters or conditions shown
               - Data representation methods

            3. Main Findings:
               - Key results demonstrated
               - Quantitative measurements
               - Comparative analyses
               - Statistical significance

            4. Contextual Integration:
               - How the figure supports main arguments
               - References to the figure in main text
               - Connection to other results
               - Implications of findings

            Return the analysis in this JSON format:
            {{
                "reference": "Figure X",
                "description": "2-3 sentence comprehensive description",
                "technical_details": "specific methodological and technical aspects",
                "findings": "key results and measurements",
                "context": "relevance to main arguments",
                "panel_descriptions": ["description of panel a", "description of panel b", ...] (if applicable)
            }}

            Text:
            {text_content}
            """

            context_response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at analyzing scientific figures and extracting their complete context. 
                        Focus on technical accuracy and quantitative details while maintaining clarity."""
                    },
                    {"role": "user", "content": context_prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            # Parse the JSON response
            figure_context = json.loads(context_response.choices[0].message.content)
            return figure_context
            
        except Exception as e:
            logger.error(f"Error extracting figure context: {str(e)}")
            return {
                "reference": figure_ref,
                "description": f"Description for {figure_ref}",
                "technical_details": "",
                "findings": "",
                "context": "",
                "panel_descriptions": []
            }