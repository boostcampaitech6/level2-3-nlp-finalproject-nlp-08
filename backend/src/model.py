from dataclass import DocumentOut, DocumentIn, doc_in_ex, doc_out_ex

def preprocess_input(context):
    return "preprocess done: " + context 

def inference(doc : DocumentIn):
    c = preprocess_input(doc.context)
    print("pre process input: ", c)
    return doc_out_ex
