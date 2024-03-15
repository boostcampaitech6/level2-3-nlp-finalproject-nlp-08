from openai import OpenAI

client = OpenAI()

def generate_question(context, answer):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "이 시스템은 제공된 본문을 기반으로 하여, 제시된 답변이 명확한 답이 될 수 있는 의문문 형식의 질문을 생성합니다. 본문에서 주요 정보를 추출하여, 이를 바탕으로 한 질문을 구성하되, 질문이 제시된 답변을 직접적으로 요구하도록 해주세요. 생성된 질문은 포멀하고 전문적인 언어를 사용해야 하며, 본문의 내용과 직접적으로 관련되어야 합니다. 질문은 정보를 명확하게 요구하는 형태이며, 사용자가 이해하기 쉬워야 합니다."},
            {"role": "user", "content": f"본문:{context}, 답변: {answer}"}
        ]
    )

    question = completion.choices[0].message.content

    return question