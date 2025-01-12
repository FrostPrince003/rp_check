# from phi.agent import Agent
# from phi.model.groq import Groq

# class NoveltyAgent:
#     def __init__(self):
#         self.agent = Agent(
#             model=Groq(id="llama-3.3-70b-versatile"),
#             markdown=True
#         )

#     def analyze(self, text):
#         """
#         Assess the novelty of the research paper.
#         Args:
#             text (str): Preprocessed text of the paper.
#         Returns:
#             dict: Score and explanation for novelty.
#         """
#         prompt = (
#             "Evaluate the novelty of the following research paper. "
#             "Provide a score between 0 and 1 (1 being highly novel) "
#             "and a brief explanation.\n\n"
#             f"{text}"
#         )
#         response = self.agent.run(prompt)
#         return self._parse_response(response)

#     def _parse_response(self, response):
#         """
#         Parse the agent's response to extract the score and explanation.
#         """
#         content = response.content.strip()
#         try:
#             score = float(content.split("Score:")[1].split()[0])
#             explanation = content.split("Explanation:")[1].strip()
#         except IndexError:
#             score = 0.0
#             explanation = "Failed to parse the response."
#         return {"score": score, "explanation": explanation}




import requests

class NoveltyAgent:
    def __init__(self, base_url="http://localhost:11434"):
        """
        Initialize the NoveltyAgent to interface with the Ollama application.
        Args:
            base_url (str): The base URL for the Ollama server. Default is "http://localhost:11434".
        """
        self.base_url = base_url

    def analyze(self, text):
        """
        Assess the novelty of the research paper.
        Args:
            text (str): Preprocessed text of the paper.
        Returns:
            dict: Score and explanation for novelty.
        """
        prompt = (
            "Evaluate the novelty of the following research paper. "
            "Provide a score between 0 and 1 (1 being highly novel) "
            "and a brief explanation.\n\n"
            f"{text}"
        )
        response = self._run_ollama(prompt)
        return self._parse_response(response)

    def _run_ollama(self, prompt):
        """
        Send a prompt to the Ollama application and get a response.
        Args:
            prompt (str): The input prompt for the model.
        Returns:
            dict: The JSON response from the Ollama application.
        """
        url = f"{self.base_url}/api/completion"
        payload = {
            "model": "llama-3.2",  # Specify the model you are running
            "prompt": prompt
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def _parse_response(self, response):
        """
        Parse the Ollama response to extract the score and explanation.
        Args:
            response (dict): The raw response from Ollama.
        Returns:
            dict: Parsed score and explanation.
        """
        if "error" in response:
            return {"score": 0.0, "explanation": response["error"]}
        
        content = response.get("completion", "").strip()
        try:
            score = float(content.split("Score:")[1].split()[0])
            explanation = content.split("Explanation:")[1].strip()
        except IndexError:
            score = 0.0
            explanation = "Failed to parse the response."
        return {"score": score, "explanation": explanation}
