# Import a data analytics package
import pandas as pd
# Read the VMI account data
df = pd.read_csv('/home/stephen/Desktop/candyVMI.csv')

order = [('kit kat', 31, 16), ('milk duds ', 14, 15), ('rolo', 12, 13), ('heath', 12, 1), ('whoppers', 22, 14), ("reese's", 12, 16), ('bulk almonds á(shavedá)', 7, 13), ('bulk sunflower seeds', 8, 6), ('cammomile tea', 4, 36), ('berry tea', 33, 0)]

report = []
# Iterate through each item in the order
for item in order:
    # Iterate through each item in the VMI account
    for vmiItem in df.values:
        # Check if the description matches
        if vmiItem[2] == item[0]:
            reportLine = []
            # Part #
            reportLine.append(vmiItem[0])
            # Description
            reportLine.append(vmiItem[2])
            # On Hand Quantity
            reportLine.append(item[1])
            # Min
            reportLine.append(vmiItem[4])
            # Max
            reportLine.append(vmiItem[3])
            # Quantity Ordered
            reportLine.append(item[2])
            # Price each
            reportLine.append(vmiItem[8])

    report.append(reportLine)

reportDF = pd.DataFrame(report)

reportDF.to_csv('/home/stephen/Desktop/report.csv')
