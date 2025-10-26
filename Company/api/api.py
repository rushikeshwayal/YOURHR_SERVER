from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Company.model.model import Company
from Company.schema.schema import CompanyCreate, CompanyUpdate, CompanyResponse
from database import get_db
from typing import List
import uuid

router = APIRouter()


# ✅ Create a new company
@router.post("/post/companies", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    new_company = Company(
        company_id=str(uuid.uuid4()),
        user_email=company.user_email,
        name=company.name,
        company_type=company.company_type,
        ceo_name=company.ceo_name,
        ceo_image_url=str(company.ceo_image_url) if company.ceo_image_url else None,
        description=company.description,
        industry=company.industry,
        mission=company.mission,
        vision=company.vision,
        goals=company.goals,
        website=str(company.website) if company.website else None,
        phone_number=company.phone_number,
        address=company.address,
        city=company.city,
        state=company.state,
        country=company.country,
        founded_year=company.founded_year,
        employee_count=company.employee_count,
        linkedin_url=str(company.linkedin_url) if company.linkedin_url else None,
        logo_url=str(company.logo_url) if company.logo_url else None,
    )

    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company


# ✅ Get all companies
@router.get("/get/companies", response_model=List[CompanyResponse])
async def get_all_companies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company))
    companies = result.scalars().all()
    return companies


# ✅ Get company by company_id
@router.get("/get/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.company_id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


# ✅ Get companies by user_email
@router.get("/get/companies/user/{user_email}", response_model=List[CompanyResponse])
async def get_companies_by_user(user_email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.user_email == user_email))
    companies = result.scalars().all()
    return companies


# ✅ Update company info
@router.put("/put/companies/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: str, updates: CompanyUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.company_id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in updates.dict(exclude_unset=True).items():
        # Ensure URLs are stored as strings
        if key in ["website", "linkedin_url", "logo_url", "ceo_image_url"] and value is not None:
            setattr(company, key, str(value))
        else:
            setattr(company, key, value)    

    await db.commit()
    await db.refresh(company)
    return company


# ✅ Delete a company
@router.delete("/delete/companies/{company_id}")
async def delete_company(company_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.company_id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    await db.delete(company)
    await db.commit()
    return {"message": "Company deleted successfully"}
