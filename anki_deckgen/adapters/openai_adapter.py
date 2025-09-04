class OpenAIAdapter:
    def __init__(self, client, model: str):
        self.client = client
        self.model = model        

    def execute_gpt_query(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.responses.create(
                # model="gpt-5-nano",
                model = self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )
        except Exception as e:
            raise RuntimeError(f"Failed to prompt: {e}") from e
        return response.output_text.strip()
