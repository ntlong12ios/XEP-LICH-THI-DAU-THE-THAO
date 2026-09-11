import pandas as pd
from database import SessionLocal, engine
import models
import os
import sys

def run_import(file_obj=None):
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    db.query(models.Match).delete()
    db.query(models.BracketSlot).delete()
    db.query(models.Athlete).delete()
    db.query(models.Team).delete()
    db.query(models.Category).delete()
    db.commit()

    sys.stdout.reconfigure(encoding='utf-8')
    if file_obj:
        xls = pd.ExcelFile(file_obj)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = [f for f in os.listdir(base_dir) if f.endswith('.xlsx') and 'Agenda' not in f and not f.startswith('~')][0]
        full_path = os.path.join(base_dir, file_path)
        xls = pd.ExcelFile(full_path)
    categories_cache = {}

    def get_or_create_category(name, sport):
        if name not in categories_cache:
            cat = db.query(models.Category).filter_by(name=name).first()
            if not cat:
                cat = models.Category(name=name, sport=sport)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            categories_cache[name] = cat
        return categories_cache[name]

    if "BĐ 28.08" in xls.sheet_names:
        df_bd = pd.read_excel(full_path, sheet_name="BĐ 28.08")
        for index in range(3, len(df_bd)):
            row = df_bd.iloc[index]
            ma_doi = str(row.iloc[2]).strip()
            noi_dung = str(row.iloc[3]).strip()
            if noi_dung.lower() == 'bóng đá nam':
                noi_dung = 'Bóng đá nam'
            ten_doan = str(row.iloc[4]).strip()
            ten_ca_nhan = str(row.iloc[6]).strip()
            nguoi_lien_he = str(row.iloc[8]).strip() if len(row) > 8 else ''
            sdt = str(row.iloc[9]).strip() if len(row) > 9 else ''
            
            if noi_dung == 'nan' and ten_ca_nhan == 'nan':
                continue
                
            cat = None
            if noi_dung and noi_dung != 'nan':
                cat = get_or_create_category(noi_dung, "Bóng đá")
            
            if ten_doan and ten_doan != 'nan':
                current_team = models.Team(
                    name=ten_doan,
                    draw_code=ma_doi if ma_doi != 'nan' else None,
                    contact_name=nguoi_lien_he if nguoi_lien_he != 'nan' else None,
                    contact_phone=sdt if sdt != 'nan' else None,
                    category_id=cat.id if cat else None
                )
                db.add(current_team)
                db.commit()
                db.refresh(current_team)
                
            if current_team and ten_ca_nhan and ten_ca_nhan != 'nan':
                athlete = models.Athlete(name=ten_ca_nhan, team_id=current_team.id)
                db.add(athlete)
        db.commit()

    if "Pick 28.08" in xls.sheet_names:
        df_pick = pd.read_excel(full_path, sheet_name="Pick 28.08")
        for index in range(3, len(df_pick)):
            row = df_pick.iloc[index]
            ma_doi = str(row.iloc[2]).strip()
            noi_dung = str(row.iloc[3]).strip()
            if noi_dung.lower() == 'bóng đá nam':
                noi_dung = 'Bóng đá nam'
            ten_doan = str(row.iloc[4]).strip()
            ten_vdv1 = str(row.iloc[6]).strip()
            ten_vdv2 = str(row.iloc[7]).strip()
            nguoi_lien_he = str(row.iloc[9]).strip() if len(row) > 9 else ''
            sdt = str(row.iloc[10]).strip() if len(row) > 10 else ''
            
            if noi_dung == 'nan' and ten_vdv1 == 'nan':
                continue
                
            if noi_dung and noi_dung != 'nan':
                cat = get_or_create_category(noi_dung, "Pickleball")
                
                team_name = f"{ten_vdv1} & {ten_vdv2}"
                if ten_doan and ten_doan != 'nan' and ten_doan != '(cá nhân)':
                    team_name = f"{ten_doan} ({team_name})"
                    
                team = models.Team(
                    name=team_name,
                    draw_code=ma_doi if ma_doi != 'nan' else None,
                    contact_name=nguoi_lien_he if nguoi_lien_he != 'nan' else None,
                    contact_phone=sdt if sdt != 'nan' else None,
                    category_id=cat.id
                )
                db.add(team)
                db.commit()
                db.refresh(team)
                
                if ten_vdv1 and ten_vdv1 != 'nan':
                    db.add(models.Athlete(name=ten_vdv1, team_id=team.id))
                if ten_vdv2 and ten_vdv2 != 'nan':
                    db.add(models.Athlete(name=ten_vdv2, team_id=team.id))
        db.commit()
    db.close()

if __name__ == "__main__":
    run_import()
