from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactRequest, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(offset, limit, db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(query: str, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, offset, limit, db)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse])
async def find_birthdays(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = await repository_contacts.find_contacts_by_birthday(offset, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactRequest, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactRequest, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
