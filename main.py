import os
import json
from agents.Coherence_agent import CoherenceAgent
from agents.Ethics_agent import EthicsAgent
from agents.Novelty_agent import NoveltyAgent
from dotenv import load_dotenv
load_dotenv()

# Initialize agents
coherence_agent = CoherenceAgent()
ethics_agent = EthicsAgent()
novelty_agent = NoveltyAgent()

# Define directories
preprocessed_dir = "Data/preprocessed_text"
output_file = "Data/evaluation_results.json"

# Define scoring thresholds (based on labeled data insights)
PUBLISHABLE_THRESHOLD = 0.75  # Minimum average score required for publishability

def evaluate_paper(file_path):
    """
    Evaluate a single research paper using all agents.
    Args:
        file_path (str): Path to the preprocessed text file.
    Returns:
        dict: Evaluation results from all agents.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Run agents
    coherence_result = coherence_agent.analyze(text)
    # ethics_result = ethics_agent.analyze(text)
    # novelty_result = novelty_agent.analyze(text)

    # Combine results
    combined_score = (
        coherence_result["score"] 
        # ethics_result["score"] +
        # novelty_result["score"]
    ) / 3  # Average score

    # Determine publishability
    is_publishable = combined_score >= PUBLISHABLE_THRESHOLD

    return {
        "filename": os.path.basename(file_path),
        "coherence": coherence_result,
        # "ethics": ethics_result,
        # "novelty": novelty_result,
        "average_score": combined_score,
        "is_publishable": is_publishable
    }

def main():
    """
    Main function to process all preprocessed papers and save results.
    """
    results = []

    # Process each file in the preprocessed directory
    for filename in os.listdir(preprocessed_dir):
        file_path = os.path.join(preprocessed_dir, filename)
        if filename.endswith(".txt") and filename == "P006.txt":
            try:
                print(f"Evaluating {filename}...")
                evaluation = evaluate_paper(file_path)
                results.append(evaluation)
            except Exception as e:
                print(f"Error evaluating {filename}: {e}")


    # Save results to a JSON file
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4)

    print(f"Evaluation completed. Results saved to {output_file}")

if __name__ == "__main__":
    main()

# import os
# import json
# from agents.Coherence_agent import CoherenceAgent
# from agents.Ethics_agent import EthicsAgent
# from agents.Novelty_agent import NoveltyAgent
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize agents
# coherence_agent = CoherenceAgent()
# ethics_agent = EthicsAgent()
# novelty_agent = NoveltyAgent()

# # Define directories
# preprocessed_dir = "Data/preprocessed_text"
# output_file = "Data/evaluation_results.json"

# # Define scoring thresholds (based on labeled data insights)
# PUBLISHABLE_THRESHOLD = 0.75  # Minimum average score required for publishability

# def evaluate_paper(file_path):
#     """
#     Evaluate a single research paper using all agents.
#     Args:
#         file_path (str): Path to the preprocessed text file.
#     Returns:
#         dict: Evaluation results from all agents.
#     """
#     with open(file_path, "r", encoding="utf-8") as file:
#         text = file.read()

#     # Run agents with error handling and debugging logs
#     try:
#         coherence_result = coherence_agent.analyze(text)
#     except Exception as e:
#         print(f"Error in coherence agent: {e}")
#         coherence_result = {"score": 0, "error": str(e)}

#     try:
#         ethics_result = ethics_agent.analyze(text)
#     except Exception as e:
#         print(f"Error in ethics agent: {e}")
#         ethics_result = {"score": 0, "error": str(e)}

#     try:
#         novelty_result = novelty_agent.analyze(text)
#     except Exception as e:
#         print(f"Error in novelty agent: {e}")
#         novelty_result = {"score": 0, "error": str(e)}

#     # Combine results - Calculate average score
#     combined_score = (
#         coherence_result["score"] + 
#         ethics_result["score"] + 
#         novelty_result["score"]
#     ) / 3  # Average score

#     # Determine publishability
#     is_publishable = combined_score >= PUBLISHABLE_THRESHOLD

#     return {
#         "filename": os.path.basename(file_path),
#         "coherence": coherence_result,
#         "ethics": ethics_result,
#         "novelty": novelty_result,
#         "average_score": combined_score,
#         "is_publishable": is_publishable
#     }

# def main():
#     """
#     Main function to process all preprocessed papers and save results.
#     """
#     results = []

#     # Process each file in the preprocessed directory
#     for filename in os.listdir(preprocessed_dir):
#         file_path = os.path.join(preprocessed_dir, filename)
#         if filename.endswith(".txt") and filename=="P006.txt":  # Process all text files
#             print(f"Evaluating {filename}...")
#             evaluation = evaluate_paper(file_path)
#             results.append(evaluation)

#     # Save results to a JSON file
#     with open(output_file, "w", encoding="utf-8") as outfile:
#         json.dump(results, outfile, indent=4)

#     print(f"Evaluation completed. Results saved to {output_file}")

# if __name__ == "__main__":
#     main()
