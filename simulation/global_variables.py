import threading


class GlobalVariables:
    ges_autos = 0
    ges_kWh = 0
    ges_dauer = 0
    fertig = False
    lock = threading.Lock()
