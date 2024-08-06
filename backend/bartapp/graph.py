class Stop():
    def __init__(self, stop_id, route_ids):
        self.stop_id = stop_id
        self.route_ids = route_ids
        self.connections = None

    def __str__(self):
        return self.stop_id

MLBR = Stop('MLBR', ['1', '2', '7', '8'])
SFIA = Stop('SFIA', ['1', '2', '7', '8'])
SBRN = Stop('SBRN', ['1', '2', '7', '8'])
SSAN = Stop('SSAN', ['1', '2', '7', '8'])
COLM = Stop('COLM', ['1', '2', '7', '8'])
DALY = Stop('DALY', ['1', '2', '5', '6', '7', '8', '11', '12'])
BALB = Stop('BALB', ['1', '2', '5', '6', '7', '8', '11', '12'])
GLEN = Stop('GLEN', ['1', '2', '5', '6', '7', '8', '11', '12'])
_24TH = Stop('24TH', ['1', '2', '5', '6', '7', '8', '11', '12'])
_16TH = Stop('16TH', ['1', '2', '5', '6', '7', '8', '11', '12'])
CIVIC = Stop('CIVC', ['1', '2', '5', '6', '7', '8', '11', '12'])
POWL = Stop('POWL', ['1', '2', '5', '6', '7', '8', '11', '12'])
MONT = Stop('MONT', ['1', '2', '5', '6', '7', '8', '11', '12'])
EMBR = Stop('EMBR', ['1', '2', '5', '6', '7', '8', '11', '12'])
WOAK = Stop('WOAK', ['1', '2', '5', '6', '7', '8', '11', '12'])

_19TH = Stop('19TH', ['1', '2', '3', '4', '7', '8'])
_12TH = Stop('12TH', ['1', '2', '3', '4', '7', '8'])
MCAR = Stop('MCAR', ['1', '2', '3', '4', '7', '8'])
ASHB = Stop('ASHB', ['1', '2', '3', '4', '7', '8'])
DBRK = Stop('DBRK', ['1', '2', '3', '4', '7', '8'])
NBRK = Stop('NBRK', ['1', '2', '3', '4', '7', '8'])
PLZA = Stop('PLZA', ['1', '2', '3', '4', '7', '8'])
DELN = Stop('DELN', ['1', '2', '3', '4', '7', '8'])
RICH = Stop('RICH', ['1', '2', '3', '4', '7', '8'])

ROCK = Stop('ROCK', ['3', '4', '7', '8'])
ORIN = Stop('ORIN', ['3', '4', '7', '8'])
LAFY = Stop('LAFY', ['3', '4', '7', '8'])
WCRK = Stop('WCRK', ['3', '4', '7', '8'])
PHIL = Stop('PHIL', ['3', '4', '7', '8'])
CONC = Stop('CONC', ['3', '4', '7', '8'])
NCON = Stop('NCON', ['3', '4', '7', '8'])
PITT = Stop('PITT', ['3', '4', '7', '8'])
PTCR = Stop('PTCR', ['3', '4', '7', '8'])
ANTC = Stop('ANTC', ['3', '4', '7', '8'])

FTVL = Stop('FTVL', ['3', '4', '5', '6', '11', '12'])
LAKE = Stop('LAKE', ['3', '4', '5', '6', '11', '12'])
COLS = Stop('COLS', ['3', '4', '5', '6', '11', '12'])
SANL = Stop('SANL', ['3', '4', '5', '6', '11', '12'])
BAYF = Stop('BAYF', ['3', '4', '5', '6', '11', '12'])
CAST = Stop('CAST', ['3', '4', '5', '6', '11', '12'])
WDUB = Stop('WDUB', ['3', '4', '5', '6', '11', '12'])
DUBL = Stop('DUBL', ['3', '4', '5', '6', '11', '12'])

CAST = Stop('CAST', ['11', '12'])
WDUB = Stop('WDUB', ['11', '12'])
DUBL = Stop('DUBL', ['11', '12'])

SHAY = Stop('SHAY', ['3', '4', '5', '6'])
HAYW = Stop('HAYW', ['3', '4', '5', '6'])
UCTY = Stop('UCTY', ['3', '4', '5', '6'])
FRMT = Stop('FRMT', ['3', '4', '5', '6'])
WARM = Stop('WARM', ['3', '4', '5', '6'])
MLPT = Stop('MLPT', ['3', '4', '5', '6'])

OAKL = Stop('OAKL', ['19', '20'])

MLBR.connections = [SFIA]
SFIA.connections = [MLBR, SBRN]
SBRN.connections = [SFIA, SSAN]
SSAN.connections = [SBRN, COLM]
COLM.connections = [SSAN, DALY]
DALY.connections = [COLM, BALB]
BALB.connections = [DALY, GLEN]
GLEN.connections = [BALB, _24TH]
_24TH.connections = [GLEN, _16TH]
_16TH.connections = [_24TH, CIVIC]
CIVIC.connections = [_16TH, POWL]
POWL.connections = [CIVIC, MONT]
MONT.connections = [POWL, EMBR]
EMBR.connections = [MONT, WOAK]
WOAK.connections = [EMBR, _12TH, LAKE]

_12TH.connections = [WOAK, _19TH]
_19TH.connections = [_12TH, MCAR]
MCAR.connections = [_19TH, ASHB, ROCK]

ASHB.connections = [MCAR, DBRK]
DBRK.connections = [ASHB, NBRK]
NBRK.connections = [DBRK, PLZA]
PLZA.connections = [NBRK, DELN]
DELN.connections = [PLZA, RICH]
RICH.connections = [DELN]

ROCK.connections = [MCAR, ORIN]
ORIN.connections = [ROCK, LAFY]
LAFY.connections = [ORIN, WCRK]
WCRK.connections = [LAFY, PHIL]
PHIL.connections = [WCRK, CONC]
CONC.connections = [PHIL, NCON]
NCON.connections = [CONC, PITT]
PITT.connections = [NCON, PTCR]
PTCR.connections = [PITT, ANTC]
ANTC.connections = [PTCR]

LAKE.connections = [WOAK, FTVL, _12TH]
FTVL.connections = [LAKE, COLS]
COLS.connections = [FTVL, SANL, OAKL]
SANL.connections = [COLS, BAYF]
BAYF.connections = [SANL, CAST, HAYW]

CAST.connections = [BAYF, WDUB]
WDUB.connections = [CAST, DUBL]
DUBL.connections = [WDUB]

HAYW.connections = [SANL, SHAY]
SHAY.connections = [HAYW, UCTY]
UCTY.connections = [SHAY, FRMT]
FRMT.connections = [UCTY, WARM]
WARM.connections = [FRMT, MLPT]
MLPT.connections = [WARM]

OAKL.connections = [COLS]