from typing import Any, Dict

class MongoDBKeyTransformer:
    """
    A class to transform keys in documents for compatibility with MongoDB, including nested structures.
    MongoDB does not allow certain characters (like '.') in document keys.
    """

    @staticmethod
    def encode_key(key: str) -> str:
        """Encode a key by replacing '.' with '__dot__'."""
        return key.replace('.', '__dot__')

    @staticmethod
    def decode_key(key: str) -> str:
        """Decode a key by replacing '__dot__' with '.'."""
        return key.replace('__dot__', '.')

    @classmethod
    def encode_document(cls, document: Any) -> Any:
        """Recursively encode all keys in a document."""
        if isinstance(document, dict):
            return {cls.encode_key(k): cls.encode_document(v) for k, v in document.items() if k is not None}
        elif isinstance(document, list):
            return [cls.encode_document(item) for item in document]
        else:
            return document

    @classmethod
    def decode_document(cls, document: Any) -> Any:
        """Recursively decode all keys in a document."""
        if isinstance(document, dict):
            return {cls.decode_key(k): cls.decode_document(v) for k, v in document.items() if k is not None}
        elif isinstance(document, list):
            return [cls.decode_document(item) for item in document]
        else:
            return document


