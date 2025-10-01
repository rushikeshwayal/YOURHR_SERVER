from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List, Union
import io

from Community.model.model import Channel, Message
from Community.schema.schema import MessageResponse
from Drive.drive_utils import (
    get_authorization_url,
    exchange_code_for_credentials,
    upload_file_to_drive,
)
from google.oauth2.credentials import Credentials
from database import get_db

router = APIRouter()


# =================== Google OAuth ===================
@router.get("/auth/google")
async def auth_google():
    auth_url, state = get_authorization_url()
    return {"auth_url": auth_url}


@router.get("/oauth2callback")
async def oauth2callback(code: str):
    creds = exchange_code_for_credentials(code)
    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "expires_in": creds.expiry,
    }


# =================== Channels ===================
@router.post("/channels")
async def create_channel(name: str = Form(...), db: AsyncSession = Depends(get_db)):
    new_channel = Channel(name=name)
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return {"id": new_channel.id, "name": new_channel.name}


@router.get("/channels")
async def list_channels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Channel).order_by(Channel.created_at))
    return [{"id": c.id, "name": c.name} for c in result.scalars().all()]


# =================== Messages ===================
def process_upload_file(upload: Union[UploadFile, str, None]) -> Optional[UploadFile]:
    """
    Convert empty strings or invalid uploads to None.
    FastAPI sometimes receives empty strings when no file is uploaded via form-data.
    """
    if upload is None:
        return None
    if isinstance(upload, str):
        # Empty string or any string means no file was uploaded
        return None
    if isinstance(upload, UploadFile):
        # Check if it's a real file with a filename
        if not upload.filename or upload.filename == "":
            return None
        return upload
    return None


@router.post("/channels/{channel_id}/messages", response_model=MessageResponse)
async def post_message(
    channel_id: int,
    user_email: str = Form(...),
    access_token: str = Form(...),
    text: Optional[str] = Form(None),
    image: Union[UploadFile, str, None] = File(default=None),
    video: Union[UploadFile, str, None] = File(default=None),
    file: Union[UploadFile, str, None] = File(default=None),
    db: AsyncSession = Depends(get_db),
):
    print("\n=== POST MESSAGE DEBUG ===")
    print(f"Channel ID: {channel_id}")
    print(f"User Email: {user_email}")
    print(f"Text: {text}")
    print(f"Image raw: {image}, type: {type(image)}")
    print(f"Video raw: {video}, type: {type(video)}")
    print(f"File raw: {file}, type: {type(file)}")
    
    # Process uploads to handle empty strings
    image = process_upload_file(image)
    video = process_upload_file(video)
    file = process_upload_file(file)
    
    print(f"After processing - Image: {image}")
    print(f"After processing - Video: {video}")
    print(f"After processing - File: {file}")

    # Check channel exists
    channel = await db.get(Channel, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # Validate at least one content field is provided
    if not text and not image and not video and not file:
        raise HTTPException(
            status_code=400, 
            detail="At least one of text, image, video, or file must be provided"
        )

    creds = Credentials(token=access_token)
    image_url = video_url = file_url = None

    # Upload files only if present
    if image:
        print(f"Uploading image: {image.filename}, content_type: {image.content_type}")
        try:
            content = io.BytesIO(await image.read())
            image_url = upload_file_to_drive(image.filename, content, image.content_type, creds)
            print(f"Image uploaded successfully: {image_url}")
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    if video:
        print(f"Uploading video: {video.filename}, content_type: {video.content_type}")
        try:
            content = io.BytesIO(await video.read())
            video_url = upload_file_to_drive(video.filename, content, video.content_type, creds)
            print(f"Video uploaded successfully: {video_url}")
        except Exception as e:
            print(f"Error uploading video: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to upload video: {str(e)}")

    if file:
        print(f"Uploading file: {file.filename}, content_type: {file.content_type}")
        try:
            content = io.BytesIO(await file.read())
            file_url = upload_file_to_drive(file.filename, content, file.content_type, creds)
            print(f"File uploaded successfully: {file_url}")
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    new_message = Message(
        channel_id=channel_id,
        user_email=user_email,
        text=text,
        image_url=image_url,
        video_url=video_url,
        file_url=file_url,
    )
    
    print(f"Creating message with URLs - image: {image_url}, video: {video_url}, file: {file_url}")
    
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    print(f"Message created successfully: {new_message.id}")
    print("=== END DEBUG ===\n")
    
    return new_message


@router.get("/channels/{channel_id}/messages", response_model=List[MessageResponse])
async def get_messages(channel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at)
    )
    return result.scalars().all()


# =================== File Upload Only ===================
@router.post("/upload")
async def upload_file(
    access_token: str = Form(...),
    file: UploadFile = File(...),
):
    creds = Credentials(token=access_token)
    content = io.BytesIO(await file.read())
    url = upload_file_to_drive(file.filename, content, file.content_type, creds)
    return {"url": url}