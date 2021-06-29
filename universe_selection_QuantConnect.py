from QuantConnect.Data.UniverseSelection import *
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

class LiquidUniverseSelection(QCAlgorithm):
    
    def Initialize(self):
        self.IfPrint = 1
        self.SetStartDate(2021, 6, 1)  
        self.SetEndDate(2021, 6, 1) 
        self.SetCash(100000)
        # Adding a universe based on two joint selections: self.CoarseSelectionFilter and self.FineSelectionFunction
        
        self.AddUniverse(self.CoarseSelectionFilter, self.FineSelectionFunction)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.SetSecurityInitializer(lambda x: x.SetDataNormalizationMode(DataNormalizationMode.Raw))
        self.Liquidate()
                
    def CoarseSelectionFilter(self, coarse):
        min_price = 20
        
        sortedByDollarVolume = sorted(coarse, key=lambda c: c.DollarVolume, reverse=True)
        sortedByDollarVolume_symbols = [c.Symbol for c in sortedByDollarVolume if c.Price > 0]
        self.Log ("Number of stocks before all screening is " + str(len(sortedByDollarVolume_symbols)))
        sortedByDollarVolumeMinPrice_symbols = [c.Symbol for c in sortedByDollarVolume if c.Price > min_price]
        self.Log ("Number of stocks after price screening (price>" + str(min_price) + ") " + "is " + str(len(sortedByDollarVolumeMinPrice_symbols)))
        number_to_return = round(0.7*len(sortedByDollarVolumeMinPrice_symbols))
        self.Log ("Number of stocks after price screening (price>" + str(min_price) + ") \
        and dollar volume screening (top 70%) " + "is " + str(number_to_return))
        return sortedByDollarVolume_symbols[:number_to_return]
        
    def FineSelectionFunction(self, fine):
        
        # selection based on morningstar sector code, in this example, technology code
        # see document here https://www.quantconnect.com/docs/data-library/fundamentals#Fundamentals-Asset-Classification
        
        self.BasicMaterials = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.BasicMaterials]
        self.ConsumerCyclical = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.ConsumerCyclical]
        self.FinancialServices = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.FinancialServices]
        self.RealEstate = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.RealEstate]
        self.ConsumerDefensive = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.ConsumerDefensive]
        self.Healthcare = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Healthcare]
        self.Utilities = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Utilities]
        self.CommunicationServices = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.CommunicationServices]
        self.Energy = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Energy]
        self.Industrials = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Industrials]
        self.Technology = [x.Symbol for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]

        return self.BasicMaterials
        
  
    def OnData(self, data):
        
        def FormString (SymbolList):
            OutputString = '\'' + str(SymbolList[0]).split(' ')[0] + '\''
            for SymbolInd in range(1,len(SymbolList)):
                OutputString = OutputString + ' ,' + '\'' + str(SymbolList[SymbolInd]).split(' ')[0] + '\''
            return OutputString
        
        
        if self.IfPrint == 1:
            self.Log("The highest trading dollar volume stocks (share price>20):")
            self.Log("\r\nBasicMaterials = [" + FormString(self.BasicMaterials) + "]" + "\r\n" + \
            "ConsumerCyclical = ["+ FormString(self.ConsumerCyclical) + "]" + "\r\n" + \
            "FinancialServices = ["+ FormString(self.FinancialServices) + "]" + "\r\n" + \
            "RealEstate = ["+ FormString(self.RealEstate) + "]" + "\r\n" + \
            "ConsumerDefensive = ["+ FormString(self.ConsumerDefensive) + "]" + "\r\n" + \
            "Healthcare = ["+ FormString(self.Healthcare) + "]" + "\r\n" + \
            "Utilities = ["+ FormString(self.Utilities) + "]" + "\r\n" + \
            "CommunicationServices = ["+ FormString(self.CommunicationServices) + "]" + "\r\n" + \
            "Energy = ["+ FormString(self.Energy) + "]" + "\r\n" + \
            "Industrials = ["+ FormString(self.Industrials) + "]" + "\r\n" + \
            "Technology = ["+ FormString(self.Technology) + "]")
            self.IfPrint = 0