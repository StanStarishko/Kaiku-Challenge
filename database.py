import json
import os
from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from models import Startup, AcceptanceStatus


class Database:
    def __init__(self):
        self.startups: Dict[str, Startup] = {}
        self._load_initial_data()

    def _load_initial_data(self):
        """Load initial data from JSON file if available"""
        data_path = os.path.join(os.path.dirname(__file__), "static", "data", "challenge3_data.json")
        print(data_path)
        if os.path.exists(data_path):
            try:
                with open(data_path, "r") as f:
                    startup_data = json.load(f)
                    
                for item in startup_data:
                    # Convert to Startup model
                    startup = Startup(**item)
                    # Initialize status as PENDING for all loaded startups
                    startup.status = AcceptanceStatus.PENDING
                    self.startups[str(startup.id)] = startup
                    
                print(f"Loaded {len(startup_data)} startups from file")
            except Exception as e:
                print(f"Error: loading startup data: {e}")
                # Initialize with empty data if file can't be loaded
                self.startups = {}
        else:
            print("Error: data not found")

    def get_all_startups(self) -> List[Startup]:
        """Return all startups"""
        return list(self.startups.values())

    def get_startup_by_id(self, startup_id: UUID) -> Optional[Startup]:
        """Get a specific startup by ID"""
        return self.startups.get(str(startup_id))

    def create_startup(self, startup: Startup) -> Startup:
        """Create a new startup"""
        startup.createdAt = datetime.now()
        self.startups[str(startup.id)] = startup
        return startup

    def update_startup(self, startup_id: UUID, status: AcceptanceStatus) -> Optional[Startup]:
        """Update startup status"""
        if str(startup_id) in self.startups:
            startup = self.startups[str(startup_id)]
            startup.status = status
            startup.updatedAt = datetime.now()
            return startup
        return None

    def get_accepted_startups(self) -> List[Startup]:
        """Get all accepted startups"""
        return [s for s in self.startups.values() if s.status == AcceptanceStatus.ACCEPTED]

    def get_rejected_startups(self) -> List[Startup]:
        """Get all rejected startups"""
        return [s for s in self.startups.values() if s.status == AcceptanceStatus.REJECTED]

    def get_pending_startups(self) -> List[Startup]:
        """Get all pending startups"""
        return [s for s in self.startups.values() if s.status == AcceptanceStatus.PENDING]


# Create a singleton instance
db = Database()