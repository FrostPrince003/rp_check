from phi.agent import Agent
from phi.model.ollama import Ollama
import json


class CoherenceAgent:
    def __init__(self):
        """
        Initialize the CoherenceAgent with the Ollama model.
        """
        try:
            self.agent = Agent(
                model=Ollama(id="llama3.2"),  # Initialize the Ollama model
                markdown=True  # Ensure markdown rendering if needed
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing the agent: {str(e)}")

    def _parse_response(self, response):
        """
        Extract the score and explanation from the response string.
        Args:
            response (str): Raw response string from the model.
        Returns:
            dict: Parsed response with 'score' and 'explanation'.
        """
        try:
            # Extract JSON-like portion of the response
            start_index = response.find("{")
            end_index = response.rfind("}") + 1
            json_part = response[start_index:end_index]

            # Parse the JSON
            result = json.loads(response)

            # Return the parsed output
            return {
                "score": result.get("score", 0),
                "explanation": result.get("explanation", "No explanation provided.")
            }
        except Exception as e:
            raise ValueError(f"Error parsing the response: {response}. Details: {str(e)}")

    def analyze(self, text, chunk_size=5000):
        """
        Analyze the coherence of the research paper in manageable chunks.
        Args:
            text (str): Preprocessed text of the paper.
            chunk_size (int): Maximum size of each chunk for analysis. Default is 5000 tokens.
        Returns:
            dict: Aggregated coherence score and detailed explanations for all chunks.
        """
        def chunk_text(text, chunk_size):
            """
            Split the text into smaller chunks.
            Args:
                text (str): Text to be split.
                chunk_size (int): Size of each chunk.
            Returns:
                list: List of text chunks.
            """
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        chunks = chunk_text(text, chunk_size)
        aggregated_score = 0
        explanations = []

        for i, chunk in enumerate(chunks):
            # Formulate the prompt
            prompt = (
                f"You are an advanced research analysis model. You are tasked with evaluating the coherence "
                f"of a research paper, but since the paper is large, it has been divided into smaller chunks "
                f"for analysis. You are evaluating chunk {i+1} of {len(chunks)}.\n\n"
                f"When analyzing this chunk, consider it as part of the larger document. Focus on:\n"
                f"- Logical flow within this chunk\n"
                f"- Clarity of arguments presented here\n"
                f"- Consistency in terminology, tone, and progression of ideas with respect to a broader narrative.\n\n"
                f"Provide the following:\n"
                f"- A coherence score between 0 and 1 (1 being highly coherent)\n"
                f"- 3 key takeaways in a concise explanation justifying your evaluation.\n\n"
                f"Research Paper Chunk {i+1}/{len(chunks)}:\n\n{chunk}\n\n"
                f"Please provide your output in the following JSON format:\n"
                f"{{\n"
                f"  \"score\": <coherence_score>,\n"
                f"  \"explanation\": \"<concise_justification_in_three_key_takeaways>\"\n"
                f"}}"
            )

            try:
                # Get the response
                response = self.agent.run(prompt)

                # Debugging: Log raw response (you can remove or comment this once the code works)
                # print(f"DEBUG: Response for chunk {i+1}:\n{response}\n")

                if not response:
                    explanations.append(f"Chunk {i+1}: No response returned by the model.")
                    continue

                # Parse the response
                result = self._parse_response(response)
                aggregated_score += result.get("score", 0)
                explanations.append(f"Chunk {i+1}: {result['explanation']}")
            except Exception as e:
                explanations.append(f"Chunk {i+1}: Error occurred - {str(e)}")
                continue

        # Calculate the average coherence score
        final_score = aggregated_score / len(chunks) if chunks else 0

        # Combine explanations into a single output
        detailed_explanation = "\n\n".join(explanations)

        return {"score": final_score, "explanation": detailed_explanation}


# # Input text
# text = '''The chunk presents a clear argument for the importance of cognitive load modeling in autonomous car cockpits, highlighting its potential to enhance safety, efficiency, and user satisfaction.
# The author effectively utilizes transitional phrases and cohesive language to connect the ideas presented in this chunk to those in the broader narrative, creating a smooth flow of arguments.
# However, some sentences seem disconnected from each other, particularly towards the end, where the discussion of chaotic fractal theory feels somewhat out of place in relation to the rest of the text.'''

# # Create an instance and analyze
# agent = CoherenceAgent()
# result = agent.analyze(text)

# # Output results
# print("Coherence Analysis Results:", result)
