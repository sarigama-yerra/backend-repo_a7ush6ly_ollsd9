import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import MenuItem, Inquiry

app = FastAPI(title="Flavor Factory API", description="Backend for Flavor Factory Restaurant website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Flavor Factory backend is running"}

@app.get("/locations")
def get_locations():
    return {
        "brand": "Flavor Factory",
        "cities": [
            {"city": "Lubumbashi", "country": "DR Congo"},
            {"city": "Johannesburg", "country": "South Africa"},
            {"city": "Ottawa", "country": "Canada"},
        ]
    }

@app.get("/menu", response_model=List[MenuItem])
def list_menu(category: Optional[str] = None, drive_thru_only: bool = False):
    try:
        filt = {}
        if category:
            filt["category"] = category
        if drive_thru_only:
            filt["is_drive_thru_friendly"] = True
        docs = get_documents("menuitem", filt, limit=200)
        # Convert Mongo documents to plain dicts with proper fields
        items: List[MenuItem] = []
        for d in docs:
            d.pop("_id", None)
            items.append(MenuItem(**d))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/inquiry")
def create_inquiry(inquiry: Inquiry):
    try:
        _id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
