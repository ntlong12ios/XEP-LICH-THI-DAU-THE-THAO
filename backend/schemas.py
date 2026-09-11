from pydantic import BaseModel
from typing import List, Optional

class AthleteBase(BaseModel):
    name: str

class Athlete(AthleteBase):
    id: int
    team_id: int
    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    draw_code: Optional[str] = None

class Team(TeamBase):
    id: int
    category_id: int
    athletes: List[Athlete] = []
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    sport: str

class Category(CategoryBase):
    id: int
    teams: List[Team] = []
    class Config:
        from_attributes = True

class GenerateBracketRequest(BaseModel):
    format: str = "knockout" # "knockout" or "round_robin"
    num_groups: Optional[int] = None

class BracketSlotBase(BaseModel):
    slot_code: str
    round_number: int
    match_number: int
    slot_index: int
    position_in_match: int
    label: Optional[str] = None

class BracketSlot(BracketSlotBase):
    id: int
    category_id: int
    team_id: Optional[int] = None
    team: Optional[Team] = None
    class Config:
        from_attributes = True

class AssignTeamRequest(BaseModel):
    team_id: Optional[int] = None

class MatchBase(BaseModel):
    match_code: str
    team1_id: Optional[int] = None
    team2_id: Optional[int] = None
    score1: Optional[int] = None
    score2: Optional[int] = None
    status: str
    next_match_id: Optional[int] = None
    loser_next_match_id: Optional[int] = None
    scheduled_time: Optional[str] = None
    court: Optional[str] = None

class Match(MatchBase):
    id: int
    category_id: int
    team1: Optional[Team] = None
    team2: Optional[Team] = None
    class Config:
        from_attributes = True

class UpdateScoreRequest(BaseModel):
    score1: Optional[int] = None
    score2: Optional[int] = None

class UpdateScheduleRequest(BaseModel):
    scheduled_time: Optional[str] = None
    court: Optional[str] = None
