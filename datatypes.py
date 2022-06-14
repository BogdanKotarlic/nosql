from datetime import datetime

def sql_to_python(values, datatypes):
    for i, v in enumerate(values):
        if datatypes[i][0].split("(")[0].lower()=="int":
            values[i]=int(v)
        elif datatypes[i][0].split("(")[0].lower()=="bigint":
            values[i]=int(v)
        elif datatypes[i][0].split("(")[0].lower()=="smallint":
            values[i]=int(v)
        elif datatypes[i][0].split("(")[0].lower()=="numeric":
            values[i]=float(v)
        elif datatypes[i][0].split("(")[0].lower()=="decimal":
            values[i]=float(v)
        elif datatypes[i][0].split("(")[0].lower()=="date":
            values[i]=datetime(v)
        elif datatypes[i][0].split("(")[0].lower()=="bool":
            values[i]=bool(v)
        elif datatypes[i][0].split("(")[0].lower()=="longblob":
            values[i]=bytes(v)

    return values