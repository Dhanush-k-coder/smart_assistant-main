from transformers import pipeline

# Load text generation model
generator = pipeline("text-generation", model="gpt2")

def generate_questions(text, count=3):
    # Truncate long text for GPT-2 context window
    text = text.strip().replace("\n", " ")[:800]

    # Prompt strategy
    prompt = f"""Read the following paragraph and generate {count} comprehension questions:\n\n{text}\n\nQuestions:\n1."""
    
    output = generator(prompt, max_length=300, num_return_sequences=1, do_sample=True, temperature=0.7)[0]['generated_text']

    # Extract questions
    raw_lines = output.split("\n")
    questions = [line.strip() for line in raw_lines if line.strip().startswith(tuple("1234567890"))]

    # Fallback if model adds unexpected format
    if not questions:
        questions = output.split("?")
        questions = [q.strip() + "?" for q in questions if len(q.strip()) > 10][:count]

    return questions[:count]
