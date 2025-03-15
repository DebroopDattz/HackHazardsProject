from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from ....models.document import Document
from ....services.document_service import DocumentService
from ....core.security import get_current_user

router = APIRouter()

@router.post("/documents/")
async def create_document(
    title: str,
    department: str,
    classification_level: str,
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
) -> Document:
    # Check user permissions
    if not has_permission(current_user, f"create_document_{classification_level}"):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to create document at this classification level"
        )
    
    document = await DocumentService.create_document(
        title=title,
        department=department,
        classification_level=classification_level,
        file=file,
        created_by=current_user.id
    )
    return document

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user = Depends(get_current_user)
) -> Document:
    document = await DocumentService.get_document(document_id)
    
    # Check access permissions
    if not can_access_document(current_user, document):
        raise HTTPException(
            status_code=403,
            detail="Access denied to this document"
        )
    
    return document

@router.put("/documents/{document_id}")
async def update_document(
    document_id: str,
    title: Optional[str] = None,
    content: Optional[UploadFile] = None,
    metadata: Optional[dict] = None,
    current_user = Depends(get_current_user)
) -> Document:
    # Verify document exists and user has permission
    document = await DocumentService.get_document(document_id)
    if not can_modify_document(current_user, document):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to modify this document"
        )
    
    updated_document = await DocumentService.update_document(
        document_id=document_id,
        title=title,
        content=content,
        metadata=metadata,
        modified_by=current_user.id
    )
    return updated_document

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user = Depends(get_current_user)
):
    # Verify document exists and user has permission
    document = await DocumentService.get_document(document_id)
    if not can_delete_document(current_user, document):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to delete this document"
        )
    
    await DocumentService.delete_document(document_id)
    return {"message": "Document successfully deleted"}

@router.get("/documents/")
async def list_documents(
    department: Optional[str] = None,
    classification_level: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    current_user = Depends(get_current_user)
) -> List[Document]:
    documents = await DocumentService.list_documents(
        department=department,
        classification_level=classification_level,
        page=page,
        limit=limit,
        user=current_user
    )
    return documents 