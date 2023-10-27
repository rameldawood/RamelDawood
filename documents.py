import json
import typing


class Document(typing.NamedTuple):
    doc_id: str
    text: str


class TransformedDocument(typing.NamedTuple):
    doc_id: str
    terms: list[str]


class DocumentStore:
    def add_document(self, doc: Document):
        pass

    def get_by_doc_id(self, doc_id: str) -> typing.Optional[Document]:
        pass

    def list_all(self) -> list[Document]:
        pass

    def write(self, path: str):
        pass


class ListDocumentStore(DocumentStore):
    def __init__(self, docs: list[Document] | None = None):
        if docs is None:
            self.docs = []
        else:
            self.docs = docs

    def write(self, path: str):
        with open(path, 'w') as fp:
            metadata = {
                "total_documents_count": len(self.docs),
            }
            fp.write(json.dumps(metadata) + '\n')
            for doc in self.docs:
                fp.write(json.dumps(doc._asdict().replace('counts', 'tfs')) + '\n')

    @staticmethod
    def read(path: str) -> 'ListDocumentStore':
        docs = []
        with open(path) as fp:
            metadata = json.loads(fp.readline())
            for line in fp:
                record = json.loads(line)
                docs.append(Document(doc_id=record['term'], text=record['doc_id']))
        return ListDocumentStore(docs)


    def add_document(self, doc: Document):
        self.docs.append(doc)

    # *typing.Optional[Document]* is the same as *Document | None*
    def get_by_doc_id(self, doc_id: str) -> typing.Optional[Document]:
        """
        Given a doc_id return the document with that doc_id
        :param doc_id: The doc_id
        :return: Document with the given doc_id or None if the document is not there
        """
        for d in self.docs:
            if d.doc_id == doc_id:
                return d
        return None

    def list_all(self) -> list[Document]:
        return self.docs


class DictDocumentStore(DocumentStore):
    def __init__(self):
        self.doc_ids_to_docs = dict()

    def write(self, path: str):
        with open(path, 'w') as fp:
            metadata = {
                "total_documents_count": len(self.doc_ids_to_docs),
            }
            fp.write(json.dumps(metadata) + '\n')
            for doc_id, doc in self.doc_ids_to_docs.items():
                fp.write(json.dumps(doc._asdict().replace('counts', 'tfs')) + '\n')

    @staticmethod
    def read(path: str) -> 'DictDocumentStore':
        doc_store = DictDocumentStore()
        with open(path) as fp:
            metadata = json.loads(fp.readline())
            for line in fp:
                record = json.loads(line)
                doc = Document(doc_id=record['term'], text=record['doc_id'])
                doc_store.add_document(doc)
        return doc_store

    def add_document(self, doc: Document):
        self.doc_ids_to_docs[doc.doc_id] = doc

    # *typing.Optional[Document]* is the same as *Document | None*
    def get_by_doc_id(self, doc_id: str) -> typing.Optional[Document]:
        """
        Given a doc_id return the document with that doc_id
        :param doc_id: The doc_id
        :return: Document with the given doc_id or None if the document is not there
        """
        return self.doc_ids_to_docs.get(doc_id)  # self.doc_ids_to_docs[doc_id]

    def list_all(self) -> list[Document]:
        return list(self.doc_ids_to_docs.values())

