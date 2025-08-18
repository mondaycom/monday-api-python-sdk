from typing import Optional

from ..query_templates import get_docs_query
from ..types import MondayApiResponse, Document
from ..graphql_handler import MondayGraphQL


class DocsModule(MondayGraphQL):
    def get_document_with_blocks(self, doc_id: str) -> Optional[Document]:
        """
        Get document with all its blocks for a specific document ID.
        
        Args:
            doc_id: The document ID to fetch
            
        Returns:
            Document object with all blocks, or None if not found
        """
        all_blocks = []
        document = None
        page = 1
        
        while True:
            query = get_docs_query(doc_id, page=page)
            response: MondayApiResponse = self.execute(query)
            
            # Check if we have docs in the response
            if not response.data.docs:
                break
                
            # Get the first (and should be only) document
            doc = response.data.docs[0]
            
            # Store the document metadata on first iteration
            if document is None:
                document = doc
                
            # If no blocks, we're done
            if not doc.blocks:
                break
                
            all_blocks.extend(doc.blocks)
            
            page += 1
            
        # Update the document with all collected blocks
        if document:
            document.blocks = all_blocks
            
        return document
