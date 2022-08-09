



def get_excess_for_housemate(self, housemate: Housemate):
        savings_excess = max(housemate.savings - self.savings_threshold, 0)
        earning_excess = max(housemate.disposable_income  - housemate.fixed_costs - self.income_threshold, 0)
        excess = earning_excess + savings_excess
        return max(excess/1000, 0)