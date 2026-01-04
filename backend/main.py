from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contacts_manager import ContactsManager
from pbx_manager import PBXManager
from config import settings

app = FastAPI(title="PBX Call Manager API", version="1.0.0")

# Initialize managers
contacts_manager = ContactsManager(contacts_file="numeri.json")
pbx_manager = PBXManager(
    host=settings.PBX_HOST,
    port=settings.PBX_PORT,
    user=settings.PBX_USERNAME,
    password=settings.PBX_PASSWORD
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/api/status")
async def get_status():
    """Get PBX status"""
    is_connected = pbx_manager.is_connected()
    return {"status": "connected" if is_connected else "disconnected"}

@app.get("/api/contacts")
async def get_contacts():
    """Get list of contacts"""
    return contacts_manager.get_contacts()

@app.post("/api/call")
async def make_call(data: dict):
    """Make a call"""
    number = data.get("number")
    extension = data.get("extension")
    
    if not number:
        return {"status": "error", "message": "Number is required"}
    
    if not extension:
        return {"status": "error", "message": "Extension is required"}
    
    success = pbx_manager.originate_call(extension, number)
    if success:
        return {"status": "success", "message": f"Call from {extension} to {number} initiated"}
    else:
        return {"status": "error", "message": "Failed to initiate call"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
