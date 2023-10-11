import  indexing_process
import query_process


def print_hi(name):

    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')
    doc_store, index = indexing_process.indexing_process("msmarco_passage_dev_rel_docs.json")
    print(query_process.query_process(doc_store, index, 'Credit Card', 10))



