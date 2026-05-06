import json
import os
from pathlib import Path


class QuizGenerationError(Exception):
    pass


def get_sambanova_client():
    try:
        from sambanova import SambaNova
    except ImportError as exc:
        raise QuizGenerationError("The SambaNova SDK is not installed yet. Rebuild the Docker app after updating requirements.") from exc

    return SambaNova(
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        base_url=os.getenv("SAMBANOVA_BASE_URL", "https://api.sambanova.ai/v1"),
    )


def extract_document_text(document):
    file_path = Path(document.file.path)
    suffix = file_path.suffix.lower()

    if suffix in {".txt", ".md", ".py", ".json", ".html", ".css", ".js"}:
        return file_path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise QuizGenerationError("PDF support is not installed yet. Rebuild the Docker app after updating requirements.") from exc

        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    return file_path.read_text(encoding="utf-8", errors="ignore")


def build_quiz_prompt(document_title, level, question_count, content):
    trimmed_content = content[:16000]
    return f"""
You are a study coach helping a learner understand a document.

Task:
- Read the document content.
- Generate exactly {question_count} understanding questions.
- Match the learner level: {level}.
- Keep the questions focused on comprehension, not trivia.
- Start easy and gradually increase difficulty, but keep the full set within the {level} band.
- Include short answer guidance for each question.

Return only valid JSON with this shape:
{{
  "document_title": "string",
  "level": "{level}",
  "summary": "2-3 sentence summary",
  "questions": [
    {{
      "question": "string",
      "why_it_matters": "string",
      "answer_guidance": "string"
    }}
  ]
}}

Document title: {document_title}

Document content:
{trimmed_content}
""".strip()


def parse_quiz_response(response_text):
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
    return json.loads(cleaned)


def generate_quiz_for_document(document, level, question_count):
    api_key = os.getenv("SAMBANOVA_API_KEY")
    if not api_key:
        raise QuizGenerationError("SAMBANOVA_API_KEY is missing. Add it to your environment or .env file.")

    document_text = extract_document_text(document).strip()
    if not document_text:
        raise QuizGenerationError("The selected document does not contain readable text.")

    client = get_sambanova_client()
    model = os.getenv("SAMBANOVA_MODEL", "DeepSeek-V3.1")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful study coach that returns only valid JSON.",
                },
                {
                    "role": "user",
                    "content": build_quiz_prompt(
                        document.title,
                        level,
                        question_count,
                        document_text,
                    ),
                },
            ],
            temperature=0.1,
            top_p=0.1,
        )
    except Exception as exc:
        raise QuizGenerationError(f"Quiz generation failed: {exc}") from exc

    output_text = response.choices[0].message.content.strip()
    if not output_text:
        raise QuizGenerationError("The model returned an empty response.")

    try:
        return parse_quiz_response(output_text)
    except json.JSONDecodeError as exc:
        raise QuizGenerationError("The model response could not be parsed as quiz JSON.") from exc
