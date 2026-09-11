from sqlalchemy.orm import Session
import models
import collections
import itertools

def generate_matches(category, slots, db: Session):
    # 1. Delete existing matches
    db.query(models.Match).filter(models.Match.category_id == category.id).delete()
    db.commit()

    matches = []
    def create_match(code):
        m = models.Match(match_code=code, category_id=category.id, status="pending")
        db.add(m)
        db.commit()
        db.refresh(m)
        matches.append(m)
        return m

    # Check if slots are round-robin (any match_number has > 2 positions)
    slot_groups = collections.defaultdict(list)
    for s in slots:
        slot_groups[s.match_number].append(s)
        
    is_round_robin = any(len(g) > 2 for g in slot_groups.values())

    if category.sport == "Bóng đá":
        tk = [create_match(f"Tứ kết {i}") for i in range(1, 5)]
        bk = [create_match(f"Bán kết {i}") for i in range(1, 3)]
        ck = create_match("Chung kết")
        h3 = create_match("Tranh hạng 3")

        for i in range(4): tk[i].next_match_id = bk[i // 2].id
        for i in range(2): 
            bk[i].next_match_id = ck.id
            bk[i].loser_next_match_id = h3.id

        sorted_slots = sorted(slots, key=lambda s: (s.match_number, s.position_in_match))
        for i in range(4):
            if i*2 < len(sorted_slots): tk[i].team1_id = sorted_slots[i*2].team_id
            if i*2+1 < len(sorted_slots): tk[i].team2_id = sorted_slots[i*2+1].team_id
        db.commit()
        
    elif is_round_robin or ("nam - nữ" in category.name.lower() or "nam nữ" in category.name.lower()):
        # Sinh trận đấu vòng bảng
        # slot_groups key=1 -> Bảng A, 2 -> Bảng B...
        for match_num, grp_slots in slot_groups.items():
            grp_slots.sort(key=lambda s: s.position_in_match)
            g_label = grp_slots[0].slot_code.split('-')[0].strip() if '-' in grp_slots[0].slot_code else f"Bảng {match_num}"
            g_letter = g_label.replace("Bảng", "").strip()
            if not g_letter:
                import string
                g_letter = string.ascii_uppercase[match_num - 1] if match_num - 1 < 26 else str(match_num)
                
            n = len(grp_slots)
            pairs = list(itertools.combinations(range(n), 2))
            for (i, j) in pairs:
                t1_id = grp_slots[i].team_id
                t2_id = grp_slots[j].team_id
                code = f"{g_letter}{i+1}-{g_letter}{j+1}"
                m = create_match(code)
                m.team1_id = t1_id
                m.team2_id = t2_id
        
        # Các trận Knockout sau vòng bảng
        tk = [create_match(f"N.Nữ TK {i:02d}") for i in range(1, 5)]
        bk = [create_match(f"N.Nữ BK {i:02d}") for i in range(1, 3)]
        ck = create_match("N.Nữ CK")
        h3 = create_match("N.Nữ 3-4")

        for i in range(4): tk[i].next_match_id = bk[i // 2].id
        for i in range(2): 
            bk[i].next_match_id = ck.id
            bk[i].loser_next_match_id = h3.id
        db.commit()
        
    elif "nữ" in category.name.lower() and "nam" not in category.name.lower():
        # Pickleball Nữ 16 đội -> Double Elimination
        r1 = [create_match(f"Trận R1-{i:02d}") for i in range(1, 9)]
        r2a = [create_match(f"Trận R2-{i:02d}") for i in range(1, 5)]
        r2b = [create_match(f"Trận R2-{i+4:02d}") for i in range(1, 5)]
        r3 = [create_match(f"Trận R3-{i:02d}") for i in range(1, 5)]
        tk = [create_match(f"Nữ TK {i:02d}") for i in range(1, 5)]
        bk = [create_match(f"Nữ BK {i:02d}") for i in range(1, 3)]
        ck = create_match("Nữ CK")
        h3 = create_match("Nữ 3-4")

        for i in range(8):
            r1[i].next_match_id = r2a[i // 2].id
            r1[i].loser_next_match_id = r2b[i // 2].id
        for i in range(4):
            r2a[i].next_match_id = tk[i].id
            r2a[i].loser_next_match_id = r3[i].id
            r2b[i].next_match_id = r3[i].id
            r3[i].next_match_id = tk[i].id
            tk[i].next_match_id = bk[i // 2].id
        for i in range(2):
            bk[i].next_match_id = ck.id
            bk[i].loser_next_match_id = h3.id

        sorted_slots = sorted(slots, key=lambda s: (s.match_number, s.position_in_match))
        for i in range(8):
            if i*2 < len(sorted_slots): r1[i].team1_id = sorted_slots[i*2].team_id
            if i*2+1 < len(sorted_slots): r1[i].team2_id = sorted_slots[i*2+1].team_id
        db.commit()

    else:
        # Pickleball Nam 32 đội -> Double Elimination
        r1 = [create_match(f"Trận R1-{i:02d}") for i in range(1, 17)]
        r2a = [create_match(f"Trận R2-{i:02d}") for i in range(1, 9)] 
        r2b = [create_match(f"Trận R2-{i+8:02d}") for i in range(1, 9)] 
        r3 = [create_match(f"Trận R3-{i:02d}") for i in range(1, 9)] 
        r4 = [create_match(f"Trận R4-{i:02d}") for i in range(1, 9)] 
        tk = [create_match(f"Nam TK {i:02d}") for i in range(1, 5)]
        bk = [create_match(f"Nam BK {i:02d}") for i in range(1, 3)]
        ck = create_match("Nam CK")
        h3 = create_match("Nam 3-4")

        for i in range(16):
            r1[i].next_match_id = r2a[i // 2].id
            r1[i].loser_next_match_id = r2b[i // 2].id
        for i in range(8):
            r2a[i].next_match_id = r4[i].id
            r2a[i].loser_next_match_id = r3[i].id
            r2b[i].next_match_id = r3[i].id
            r3[i].next_match_id = r4[i].id
            r4[i].next_match_id = tk[i // 2].id
        for i in range(4):
            tk[i].next_match_id = bk[i // 2].id
        for i in range(2):
            bk[i].next_match_id = ck.id
            bk[i].loser_next_match_id = h3.id

        sorted_slots = sorted(slots, key=lambda s: (s.match_number, s.position_in_match))
        for i in range(16):
            if i*2 < len(sorted_slots): r1[i].team1_id = sorted_slots[i*2].team_id
            if i*2+1 < len(sorted_slots): r1[i].team2_id = sorted_slots[i*2+1].team_id
        db.commit()

    return len(matches)
