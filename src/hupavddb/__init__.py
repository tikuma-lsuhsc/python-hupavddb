"""Hospital Universitario Príncipe de Asturias Voice Disorders Database Reader module"""

__version__ = "0.0.0"

import pandas as pd
from os import path
import numpy as np
from glob import glob as _glob
import re, operator

# global variables
_dir = None  # database dir
_df = None  # main database table
_df_dx = None  # patient diagnosis table
_dx = None  # patient diagnoses series


def load_db(dbdir):
    """load disordered voice database

    :param dbdir: path to the cdrom drive or the directory hosting a copy of the database
    :type dbdir: str

    * This function must be called at the beginning of each Python session
    * Database is loaded from the text file found at: <dbdir>/EXCEL50/TEXT/KAYCDALL.TXT
    * Only entries with NSP files are included
    * PAT_ID of the entries without PAT_ID field uses the "FILE VOWEL 'AH'" field value
      as the PAT_ID value

    """

    global _dir, _df, _df_dx, _dx

    if _dir == dbdir:
        return

    sheets = ["Normales", "Patológicos"]

    dtypes = {
        "Archivo": "string",
        # "Fs": "UInt16",
        "Tipo": "category",
        "EGG": "boolean",
        "edad": "UInt8",
        "sexo": "category",
        "G": int,
        "R": int,
        "A": int,
        "B": int,
        "S": int,
        "Total": int,
        "Codigo": "string",
        "Patología": "category",
        "F0": float,
        "F1": float,
        "F2": float,
        # "F3": float,
        "Formantes": "category",
        "Picos": "category",
        "Jitter": "category",
        "Comentarios": "string",
    }

    _re_fs = re.compile(r"^(\d+) kHz$")


    def _fs(x):
        m = _re_fs.match(x)
        return int(m[1]) * 1000 if m else None


    def _force_float(x):
        try:
            return np.uint16(x)
        except:
            return None


    _df = pd.concat(
        [
            f
            for f in pd.read_excel(
                path.join(dbdir, "HUPA segmentada.xls"),
                sheets,
                header=1,
                dtype=dtypes,
                na_values=["?"],
                true_values=["Yes"],
                false_values=["No"],
                converters={"Fs": _fs, "F3": _force_float},
            ).values()
        ]
    )
    _dir = dbdir


def get_fields():
    """get list of all database fields

    :return: list of field names
    :rtype: list(str)
    """
    return sorted(_df.columns.values)
