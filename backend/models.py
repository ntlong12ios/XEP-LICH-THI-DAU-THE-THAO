from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sport = Column(String)  # Bóng đá, Pickleball
    teams = relationship("Team", back_populates="category")
    bracket_slots = relationship("BracketSlot", back_populates="category")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    draw_code = Column(String, nullable=True)  # Mã bốc thăm (VD: P.2Nam_01)

    category = relationship("Category", back_populates="teams")
    athletes = relationship("Athlete", back_populates="team")
    bracket_slots = relationship("BracketSlot", back_populates="team", foreign_keys="BracketSlot.team_id")

class Athlete(Base):
    __tablename__ = "athletes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="athletes")

class BracketSlot(Base):
    """Một ô trống trong sơ đồ bốc thăm. Mỗi trận có 2 slots."""
    __tablename__ = "bracket_slots"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    slot_code = Column(String)        # Mã trận: "Trận R1-01", "BĐ Nam 1"
    round_number = Column(Integer)    # Vòng: 1, 2, 3...
    match_number = Column(Integer)    # Số thứ tự trận trong vòng
    slot_index = Column(Integer)      # Thứ tự slot tổng thể (dùng để sort)
    position_in_match = Column(Integer)  # 1 hoặc 2 (trên/dưới trong 1 trận)
    label = Column(String, nullable=True)  # Nhãn hiển thị
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)  # Đội được gán

    category = relationship("Category", back_populates="bracket_slots")
    team = relationship("Team", back_populates="bracket_slots", foreign_keys=[team_id])

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    match_code = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    team1_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    team2_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    score1 = Column(Integer, nullable=True)
    score2 = Column(Integer, nullable=True)
    status = Column(String, default="pending")  # pending, playing, completed
    next_match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    loser_next_match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    scheduled_time = Column(String, nullable=True)  # Giờ thi đấu
    court = Column(String, nullable=True)  # Sân thi đấu

    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])

class AppState(Base):
    __tablename__ = "app_state"
    key = Column(String, primary_key=True, index=True)
    value = Column(String)  # Store JSON string
