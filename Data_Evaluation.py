# Using data science algorithms,
#     suggest which products should be dropped from selling in
#     the next year moving forward and which products should
#     be sold more. Should any region be given preference over
#     the other?
#     hint: look at the profitability

import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

products = {}
productTypes = []
regions = {}
regionTypes = []

with open("Data_Science_Evaluation.csv") as dataFile:  # Organize entries by product
    # Assumes "Item Time" implies unique product given that they share profitibility percentage of cost
    reader = csv.DictReader(dataFile)
    for row in reader:
        if products.get(row['Item Type']) == None:
            products[row['Item Type']] = [row]
            productTypes.append(row['Item Type'])
        else:
            products.get(row['Item Type']).append(row)

        if regions.get(row["Region"]) == None:
            regions[row["Region"]] = [row]
            regionTypes.append(row["Region"])
        else:
            regions.get(row["Region"]).append(row)


totalProfit = {}
averageProcessingTime = {}
numItems = 0
for item in productTypes:
    totalProfit[item] = 0.0
    averageProcessingTime[item] = 0
    for row in products.get(item):
        totalProfit[item] += float(row["Total Profit"])

        # Process the time from order to shipment ie. the time to process
        date_format = "%m/%d/%Y"
        orderDate = datetime.strptime(row["Order Date"], date_format)
        shipDate = datetime.strptime(row["Ship Date"], date_format)
        averageProcessingTime[item] += (shipDate-orderDate).days
        numItems += 1
    averageProcessingTime[item] /= numItems


processingTimeList = []
profitList = []
for item in productTypes:  # Given average processing time and total profit, we can plot the result to find patterns
    processingTimeList.append(averageProcessingTime[item])
    profitList.append(totalProfit[item])
#plt.scatter(processingTimeList, profitList, marker='o')
# plt.show()                # Didn't give us much that is substantial, so we will stick with profitibility


# Next, we use a simple 2-means cluster algorithm to find which products should be removed and which should be increased
profitList = []
for item in productTypes:
    profitList.append((item, totalProfit.get(item)))
profitList = sorted(profitList, key=lambda x: x[1])
cluster1 = np.random.rand()*profitList[len(profitList)-1][1]
cluster2 = np.random.rand()*profitList[len(profitList)-1][1]
cluster1Array = []
cluster2Array = []

newCluster1 = 0.0
newCluster2 = 0.0
while newCluster1 != cluster1:
    cluster1, cluster2 = newCluster1, newCluster2
    newCluster1 = 0.0
    newCluster2 = 0.0
    cluster1Array = []
    cluster2Array = []
    for profit in profitList:
        if (abs(profit[1] - cluster1) > abs(profit[1]-cluster2)):
            newCluster2 += profit[1]
            cluster2Array.append(profit)
        else:
            newCluster1 += profit[1]
            cluster1Array.append(profit)
    if len(cluster1Array) != 0:
        newCluster1 /= len(cluster1Array)
    if len(cluster2Array) != 0:
        newCluster2 /= len(cluster2Array)

print("Items to increase production:")
for item in cluster1Array:
    print(item[0])
print("\nItems to be removed:")
for item in cluster2Array:
    print(item[0])


# Next, we look by region to find more profitible regions
regionProfitability = {}
for region in regionTypes:
    regionProfitability[region] = 0.0
    for row in regions[region]:
        regionProfitability[region] += float(row["Total Profit"])
orderedRegionProfitability = sorted(
    regionProfitability.items(), key=lambda x: x[1])
x, y = zip(*orderedRegionProfitability)
plt.plot(x, y)
plt.show()

# The Following plot shows an increase by one order of magnitute
# between the Region with the largest profit (Europe) and the Smallest (North America)

# We could use k-clustering to find a breaking point, but, given that these are regions,
# it would be more important to consider the savings of removing them on a case by case basis.
# Generally, since they are much higher in profitability, I would recommend prioritizing Europe
# and Sub-Saharan Africa as a customer base.
