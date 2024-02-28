import pandas as pd


def preprocessing_dataset(dataset):
    
    train_data = pd.DataFrame(columns=['id', 'context', 'question', 'answer', 'answer_start', 'answer_type', 'classtype', 'clue_text', 'clue_start', 'clue_end'])

    for i in range(len(dataset)):
        data = dataset.iloc[i]
        id = data['id']
        context = data['context']
        question = data['question']
        answer = data['answers']['text'][0]
        answer_start = data['answers']['answer_start'][0]
        answer_type = None
        classtype = None
        clue_text = None
        clue_start = None
        clue_end = None
        train_data.loc[i] = [id, context, question, answer, answer_start, answer_type, classtype, clue_text, clue_start, clue_end]
    
    return train_data