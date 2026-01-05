import os
import boto3
import geopandas as gpd
from sqlalchemy import create_engine
import io
import logging

# הגדרת לוגים ל-CloudWatch
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# קבלת פרטי התחברות ממשתני סביבה (Best Practice)
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
TABLE_NAME = "spatial_data"

# יצירת חיבור ל-RDS
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')

def process_geojson(bucket_name, file_key):
    s3 = boto3.client('s3')
    
    try:
        logger.info(f"Starting to process file: {file_key} from bucket: {bucket_name}")
        
        # קריאת הקובץ מ-S3 לזיכרון
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read()
        
        # טעינה ל-GeoPandas לצורך ולידציה
        gdf = gpd.read_file(io.BytesIO(content))
        
        if gdf.empty:
            logger.error("File is empty or not a valid GeoJSON")
            return

        # ולידציה בסיסית - בדיקה שהגיאומטריות תקינות
        if not gdf.is_valid.all():
            logger.warning("Some geometries are invalid, attempting to fix...")
            gdf.geometry = gdf.make_valid()

        # כתיבה ל-RDS (PostGIS)
        # הפונקציה to_postgis דורשת התקנה של geoalchemy2
        gdf.to_postgis(TABLE_NAME, engine, if_exists='append', index=False)
        
        logger.info(f"Successfully loaded {len(gdf)} rows into {TABLE_NAME}")

    except Exception as e:
        logger.error(f"Error processing {file_key}: {str(e)}")
        raise e

if __name__ == "__main__":
    # כאן יבוא הקוד שיאזין ל-Events או יופעל ע"י טריגר
    pass