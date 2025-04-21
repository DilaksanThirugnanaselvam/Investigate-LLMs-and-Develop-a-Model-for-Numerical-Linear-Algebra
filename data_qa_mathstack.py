import requests
import time
import yaml

def fetch_questions(tag='numerical-linear-algebra', pages=1):
    questions = []
    for page in range(1, pages + 1):
        url = f'https://api.stackexchange.com/2.3/questions?page={page}&pagesize=10&order=desc&sort=votes&tagged={tag}&site=math&filter=withbody'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue
        data = response.json()
        for item in data['items']:
            question = {
                'question_id': item['question_id'],
                'body': item.get('body', '')
            }
            questions.append(question)
        time.sleep(1)  # Respect API rate limits
    return questions

def fetch_top_answer(question_id):
    url = f'https://api.stackexchange.com/2.3/questions/{question_id}/answers?order=desc&sort=votes&site=math&filter=withbody'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch answers for question {question_id}")
        return ''
    data = response.json()
    if data['items']:
        return data['items'][0].get('body', '')
    return ''

def save_qa_to_yaml(questions, filename='qa_pairs.yaml'):
    qa_pairs = []
    for q in questions:
        answer = fetch_top_answer(q['question_id'])
        qa_pairs.append({
            'question': q['body'],
            'answer': answer
        })
        time.sleep(1)
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(qa_pairs, f, allow_unicode=True)
    return filename

# Main workflow
questions = fetch_questions(pages=1)
qa_yaml = save_qa_to_yaml(questions)
print(f"Q&A pairs saved to: {qa_yaml}")
