import json

def load_spec(path="config files\mysql_table_reference_spec.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    # return {
    #     "offictial_languages": {
    #         "JEZ_JEZIK":"languages",
    #         "DR_IDENTIFIKATOR":"state"
    #     },
    #     "state": {
    #         "STA_DR_IDENTIFIKATOR":"composite_state",
    #         "NM_IDENTIFIKATOR":"populated_places"
    #     },
    #     "high_education_institution":{
    #         "TIP_UST":"types_of_institutions",
    #         "DR_IDENTIFIKATOR":"state",
    #         "VV_OZNAKA":"ownership_type"
    #     },
    #     "drzava":{
    #         "NM_OZNAKA": "drzavno_uredjenje"
    #     }
    # }