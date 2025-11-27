"""Utilities for loading and preparing the airline dataset used in the app."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Tuple

import pandas as pd
import requests

AIRLINE_DATA_PATH = "Airline_dataset.csv"
AIRLINES_LOOKUP_URL = "https://query.data.world/s/wpnzpdbcchgnj4vqacqww66vdhpovr?dws=00000"
AIRPORTS_URL = "https://ourairports.com/data/airports.csv"

IATA_CODES = {
    'ABE', 'ABI', 'ABQ', 'ABR', 'ABY', 'ACK', 'ACT', 'ACV', 'ACY', 'ADK', 'ADQ', 'AEX', 'AGS',
    'AKN', 'ALB', 'ALO', 'ALW', 'AMA', 'ANC', 'APN', 'ART', 'ASE', 'ATL', 'ATW', 'ATY', 'AUS',
    'AVL', 'AVP', 'AZA', 'AZO', 'BDL', 'BET', 'BFF', 'BFL', 'BFM', 'BGM', 'BGR', 'BHM', 'BIL',
    'BIS', 'BJI', 'BKG', 'BLI', 'BLV', 'BMI', 'BNA', 'BOI', 'BOS', 'BPT', 'BQK', 'BQN', 'BRD',
    'BRO', 'BRW', 'BTM', 'BTR', 'BTV', 'BUF', 'BUR', 'BWI', 'BZN', 'CAE', 'CAK', 'CDC', 'CDV',
    'CGI', 'CHA', 'CHO', 'CHS', 'CID', 'CIU', 'CKB', 'CLE', 'CLL', 'CLT', 'CMH', 'CMI', 'CMX',
    'CNY', 'COD', 'COS', 'COU', 'CPR', 'CRP', 'CRW', 'CSG', 'CVG', 'CWA', 'CYS', 'DAB', 'DAL',
    'DAY', 'DBQ', 'DCA', 'DEN', 'DFW', 'DHN', 'DIK', 'DLG', 'DLH', 'DRO', 'DRT', 'DSM', 'DTW',
    'DUT', 'DVL', 'EAR', 'EAT', 'EAU', 'ECP', 'EGE', 'EKO', 'ELM', 'ELP', 'ERI', 'ESC', 'EUG',
    'EVV', 'EWN', 'EWR', 'EYW', 'FAI', 'FAR', 'FAT', 'FAY', 'FCA', 'FLG', 'FLL', 'FLO', 'FNT',
    'FSD', 'FSM', 'FWA', 'GCC', 'GCK', 'GEG', 'GFK', 'GGG', 'GJT', 'GNV', 'GPT', 'GRB', 'GRI',
    'GRK', 'GRR', 'GSO', 'GSP', 'GST', 'GTF', 'GTR', 'GUC', 'GUM', 'HDN', 'HGR', 'HHH', 'HIB',
    'HLN', 'HNL', 'HOB', 'HOU', 'HPN', 'HRL', 'HSV', 'HTS', 'HVN', 'HYA', 'HYS', 'IAD', 'IAG',
    'IAH', 'ICT', 'IDA', 'ILM', 'IMT', 'IND', 'INL', 'IPT', 'ISN', 'ISP', 'ITH', 'ITO', 'JAC',
    'JAN', 'JAX', 'JFK', 'JHM', 'JLN', 'JMS', 'JNU', 'KOA', 'KTN', 'LAN', 'LAR', 'LAS', 'LAW',
    'LAX', 'LBB', 'LBE', 'LBF', 'LBL', 'LCH', 'LCK', 'LEX', 'LFT', 'LGA', 'LGB', 'LIH', 'LIT',
    'LNK', 'LNY', 'LRD', 'LSE', 'LWB', 'LWS', 'LYH', 'MAF', 'MBS', 'MCI', 'MCO', 'MDT', 'MDW',
    'MEI', 'MEM', 'MFE', 'MFR', 'MGM', 'MHK', 'MHT', 'MIA', 'MKE', 'MKG', 'MKK', 'MLB', 'MLI',
    'MLU', 'MMH', 'MOB', 'MOT', 'MQT', 'MRY', 'MSN', 'MSO', 'MSP', 'MSY', 'MTJ', 'MVY', 'MYR',
    'OAJ', 'OAK', 'OGD', 'OGG', 'OGS', 'OKC', 'OMA', 'OME', 'ONT', 'ORD', 'ORF', 'ORH', 'OTH',
    'OTZ', 'OWB', 'PAE', 'PAH', 'PBG', 'PBI', 'PDX', 'PGD', 'PGV', 'PHF', 'PHL', 'PHX', 'PIA',
    'PIB', 'PIE', 'PIH', 'PIR', 'PIT', 'PLN', 'PNS', 'PPG', 'PQI', 'PRC', 'PSC', 'PSE', 'PSG',
    'PSM', 'PSP', 'PUB', 'PUW', 'PVD', 'PVU', 'PWM', 'RAP', 'RDD', 'RDM', 'RDU', 'RFD', 'RHI',
    'RIC', 'RIW', 'RKS', 'RNO', 'ROA', 'ROC', 'ROW', 'RST', 'RSW', 'SAF', 'SAN', 'SAT', 'SAV',
    'SBA', 'SBN', 'SBP', 'SBY', 'SCC', 'SCE', 'SCK', 'SDF', 'SEA', 'SFB', 'SFO', 'SGF', 'SGU',
    'SHD', 'SHR', 'SHV', 'SIT', 'SJC', 'SJT', 'SJU', 'SLC', 'SLN', 'SMF', 'SMX', 'SNA', 'SPI',
    'SPN', 'SPS', 'SRQ', 'STC', 'STL', 'STS', 'STT', 'STX', 'SUN', 'SUX', 'SWF', 'SWO', 'SYR',
    'TLH', 'TOL', 'TPA', 'TRI', 'TTN', 'TUL', 'TUS', 'TVC', 'TWF', 'TXK', 'TYR', 'TYS', 'UIN',
    'USA', 'VEL', 'VLD', 'VPS', 'WRG', 'WYS', 'XNA', 'XWA', 'YAK', 'YKM', 'YUM'
}


def _load_main_dataset(dataset_path: Path) -> pd.DataFrame:
    """Read the local airline dataset and apply core cleaning steps."""

    df = pd.read_csv(dataset_path)
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%y')

    cols_to_int = ["AIRLINE_ID", "FLIGHT_NUM", "ORIGIN_SEQ_ID", "DEST_SEQ_ID"]
    df[cols_to_int] = df[cols_to_int].astype(int)

    df['DEP_DELAY'] = df['DEP_DELAY'].fillna(0)
    df['ARR_DELAY'] = df['ARR_DELAY'].fillna(0)

    df.loc[
        (df['WEATHER_DELAY'] >= 4.03) & (df['WEATHER_DELAY'] <= 4.04),
        'WEATHER_DELAY'
    ] = 0

    return df


def _load_airlines_lookup() -> pd.DataFrame:
    """Fetch the airline description lookup table."""

    return pd.read_csv(AIRLINES_LOOKUP_URL)


def _load_airports_dataset() -> pd.DataFrame:
    """Download airport metadata and keep the subset of US commercial airports."""

    response = requests.get(AIRPORTS_URL, timeout=30)
    response.raise_for_status()
    airports = pd.read_csv(StringIO(response.text))

    airports_us = airports[airports['iso_country'] == 'US'].copy()
    airports_us = airports_us[airports_us['iata_code'].isin(IATA_CODES)]

    airports_us = airports_us[[
        'iata_code', 'name', 'municipality', 'iso_region', 'latitude_deg', 'longitude_deg'
    ]].rename(columns={
        'iata_code': 'IATA',
        'name': 'Airport_Name',
        'municipality': 'City',
        'iso_region': 'State',
        'latitude_deg': 'Latitude',
        'longitude_deg': 'Longitude'
    })

    return airports_us


def load_preprocessed_data(dataset_path: str | Path = AIRLINE_DATA_PATH) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load and clean the airline dataset along with the US airports reference data.

    Returns a tuple containing the cleaned flight dataframe and the filtered airports
    dataframe that share the same IATA coverage used in the dashboards.
    """

    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path.resolve()}")

    df = _load_main_dataset(dataset_path)
    airlines_lookup = _load_airlines_lookup()
    df = df.merge(airlines_lookup, left_on='AIRLINE_ID',
                  right_on='Code', how='left')
    df = df.rename(columns={'Description': 'Airline_Name'})

    airports_us = _load_airports_dataset()

    return df, airports_us
