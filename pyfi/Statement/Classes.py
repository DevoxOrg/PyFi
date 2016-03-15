import datetime


class QifItem:
    def __init__(self, qif):
        self.order = {'num': None, 'payee': None, 'amountInSplit': None, 'memoInSplit': None, 'memo': None,
                      'date': None, 'category': None, 'amount': None, 'cleared': None, 'address': None,
                      'categoryInSplit': None}
        for part in qif:
            if len(part) > 0:
                if part[0] == "!":
                    pass
                elif part[0] == "D":
                    date = part[1:]
                    date_parts = date.split("/")
                    if len(date_parts[0]) == 1:
                        date_parts[0] = "0" + date_parts[0]
                    if len(date_parts[1]) == 1:
                        date_parts[1] = "0" + date_parts[1]
                    self.order["date"] = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                    self.textdate = date_parts[2] + "-" + date_parts[1] + "-" + date_parts[0]
                elif part[0] == "T":
                    self.order["amount"] = part[1:]
                elif part[0] == "C":
                    self.order["cleared"] = part[1:]
                elif part[0] == "P":
                    self.order["payee"] = part[1:]
                elif part[0] == "M":
                    self.order["memo"] = part[1:]
                elif part[0] == "A":
                    self.order["address"] = part[1:]
                elif part[0] == "L":
                    self.order["category"] = part[1:]
                elif part[0] == "S":
                    try:
                        self.order["categoryInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["categoryInSplit"] = [part[1:]]
                elif part[0] == "E":
                    try:
                        self.order["memoInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["memoInSplit"] = [part[1:]]
                elif part[0] == "$":
                    try:
                        self.order["amountInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["amountInSplit"] = [part[1:]]
                else:
                    pass

    def __repr__(self):
        keys = [thingy for thingy in self.order.keys() if thingy not in ["memoInSplit",
                                                                         "categoryInSplit",
                                                                         "amountInSplit"]]
        items = []
        for key in keys:
            items.append(self.order[key])

        keys = str(keys)[1:-2]
        items = str(items)[1:-2]
        return keys + "\n" + items


def make_qifs(filepath):
    qifs = []
    qif_count = 0
    with open(filepath, "r") as qif_file:
        readin = qif_file.read()
        readin.rstrip("\n")
        readin.rstrip("^")
        splitqifs = readin.split("^")
        if len(splitqifs[-1]) < 5:
            del splitqifs[-1]
        for qif in splitqifs:
            qif_count += 1
            qifs.append(QifItem(qif.split("\n")))

    return qifs
