import sys
import RecommendationsEngine as reng
recommend = reng.Recommendations(5)

# name = str(input("Enter Player Name: "))
# print("----------------Filter Values--------------------------")
# club = str(input("Enter Club Name: "))
# nation = str(input("Enter Nationality: "))
# mval = int(input("Enter Market Value: "))  # LTEqualTo

recommend.getTopKSimilar(name = "mess")
