import numpy as np
import math
from user import User
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Simulation:
    
    def __init__(self, num_men:int, num_women:int, num_swipes_per_day_men:int, num_swipes_per_day_women:int, men_formula:str, women_formula:str, num_men_premuim:int=0, num_women_premuium:int=0):
        """
        Initializes a new Simulation object.
        
        Args:
            num_men (int): Number of male users.
            num_women (int): Number of female users.
            num_swipes_per_day (int): Number of swipes allowed per user per day.
            men_formula (str): Formula to calculate attractiveness rate for men.
            women_formula (str): Formula to calculate attractiveness rate for women.
            num_men_premium (int, optional): Number of premium male users. Defaults to 0.
            num_women_premium (int, optional): Number of premium female users. Defaults to 0.
        """
        self.num_men = num_men
        self.num_women = num_women
        self.num_swipes_per_day_men = num_swipes_per_day_men
        self.num_swipes_per_day_women = num_swipes_per_day_women
        self.men_formula = self.parse_formula(men_formula)
        self.women_formula = self.parse_formula(women_formula)
        self.num_men_premuim = num_men_premuim
        self.num_women_premuium = num_women_premuium
        self.men = []
        self.women = []
        self.all = []
        self.initialize_population()
        self.plot_functions()
        
        
    def initialize_population(self):
        """
        Initializes the population of users based on the given parameters.
        """
        self.men = [
            User(
                gender='M', 
                attractiveness=np.random.uniform(0, 1),
                formula=self.men_formula,
                num_swipes=self.num_swipes_per_day_men
            )
            for _ in range(self.num_men)
            ]
        
        self.women = [
            User(
                gender='W', 
                attractiveness=np.random.uniform(0, 1),
                formula=self.women_formula,
                num_swipes=self.num_swipes_per_day_women
            )
            for _ in range(self.num_women)
            ]
        
        self.all = self.men + self.women
        
        
    def parse_formula(self, formula):
        """
        Parses the given formula to make it evaluable.
        
        Args:
            formula (str): The formula to be parsed.
            
        Returns:
            str: The parsed formula.
        """
        formula = formula.replace("^", "**")
        formula = formula.replace("pi", "math.pi")  
        formula = formula.replace("sqrt", "math.sqrt")  
        formula = formula.replace("e", "math.e")
        formula = formula.replace("sin", "math.sin")
        formula = formula.replace("tan", "math.tan")
        formula = formula.replace("asin", "math.asin")
        formula = formula.replace("acos", "math.acos")
        formula = formula.replace("atan", "math.atan")
        formula = formula.replace("sqrt", "math.sqrt") 
        formula = formula.replace("log2", "math.log2")
        formula = formula.replace("log", "math.log")
        formula = formula.replace("abs", "math.fabs")
        return formula
        
        
    def get_users_by_gender(self, gender, _same):
        """
        Retrieves users based on gender.
        
        Args:
            gender (str): The gender to filter by ('M' or 'W').
            _same (bool): If True, returns users of the same gender, otherwise returns users of the opposite gender.
            
        Returns:
            List[User]: List of users filtered by the given gender.
        """
        if gender not in ('M', 'W'):
            raise ValueError('incorrect gender')
        
        if _same:
            if gender == 'M':
                return self.men
            else:
                return self.women
        else:
            if gender == 'M':
                return self.women
            else:
                return self.men
           
            
    def simulate_day_one_person(self, user, potential_matches):
        """
        Simulates the swiping behavior of a single user for one day.
        
        Args:
            user (User): The user for whom the simulation is being run.
            potential_matches (List[User]): List of potential matches for the user.
        """
        max_swipes = min(user.left_swipes, len(potential_matches))
        for pm in np.random.choice(potential_matches, max_swipes, replace=False):
            user.left_swipes -= 1
            if np.random.uniform(0, 1) < pm.attractiveness_rate:
                user.like(pm)
            
            
    def simulate_day_one_gender(self, gender):
        """
        Simulates the swiping behavior of all users of a specific gender for one day.
        
        Args:
            gender (str): The gender to filter by ('M' or 'W').
        """
        opposite_gender = self.get_users_by_gender(gender, False)
        gender = self.get_users_by_gender(gender, True)
        for user in gender:
            self.simulate_day_one_person(user, opposite_gender)
            
            
    def simulate(self, days=1):
        """
        Simulates the swiping behavior of all users for a given number of days.
        
        Args:
            days (int, optional): Number of days to run the simulation. Defaults to 1.
        """
        for day in range(days):
            self.simulate_day_one_gender('M')
            self.simulate_day_one_gender('W')
            for user in self.all:
                user.calculate_stats()
                
        self.plot_distributions()
        
        # for user in self.all:
        #     user.refresh()
        
        
    def get_stats(self):
        """
        Retrieves statistics about likes and matches for all users.
        
        Returns:
            Dict[str, Union[float, int]]: A dictionary containing mean and median values for likes and matches for both genders.
        """
        men_stats = np.array([man.get_stats() for man in self.men])
        women_stats = np.array([woman.get_stats() for woman in self.women])
        res =  {
            'men_likes_mean': np.mean(men_stats, axis=0)[0],
            'men_likes_median': np.median(men_stats, axis=0)[0],
            'men_matches_mean': np.mean(men_stats, axis=0)[1],
            'men_matches_median': np.median(men_stats, axis=0)[1],
            'women_likes_mean': np.mean(women_stats, axis=0)[0],
            'women_likes_median': np.median(women_stats, axis=0)[0],
            'women_matches_mean': np.mean(women_stats, axis=0)[1],
            'women_matches_median': np.median(women_stats, axis=0)[1],
        }
        for user in self.all:
            user.refresh()
        return res        
    
    
    def get_stats_by_percentile(self, people, nbins):
        """
        Retrieves statistics about likes and matches for users, grouped by attractiveness percentiles.
        
        Args:
            people (List[User]): List of users for whom statistics are being retrieved.
            nbins (int): Number of bins for grouping users by attractiveness.
            
        Returns:
            Dict[str, Dict[str, float]]: A dictionary containing average likes and matches for each attractiveness percentile.
        """
        bins = {i: {'likes': [], 'matches': []} for i in range(nbins)}
        for person in people:
            attractiveness_bin = int(np.floor(person.attractiveness * nbins))
            attractiveness_bin = min(attractiveness_bin, nbins - 1)
            bins[attractiveness_bin]['likes'].append(person.num_likes)
            bins[attractiveness_bin]['matches'].append(person.num_matches)
            
        bins_ = {}
        for bin in bins:
            lower = int((bin / nbins) * 100)
            upper = int(((bin + 1) / nbins) * 100)
            bins_[f'{lower}-{upper}'] = {}
            bins_[f'{lower}-{upper}']['likes'] = np.mean(bins[bin]['likes']) if bins[bin]['likes'] else 0
            bins_[f'{lower}-{upper}']['matches'] = np.mean(bins[bin]['matches']) if bins[bin]['matches'] else 0
        return bins_
    
    
    def plot_distributions(self, path='./plots/distributions.png', nbins=10):
        """
        Plots the distributions of likes and matches for users, grouped by attractiveness percentiles.
        
        Args:
            path (str, optional): Path to save the plot. Defaults to './app/plots/distributions.png'.
            nbins (int, optional): Number of bins for grouping users by attractiveness. Defaults to 10.
        """
        stats_men = self.get_stats_by_percentile(self.men, nbins)
        stats_women = self.get_stats_by_percentile(self.women, nbins)
        data = []
        for attractiveness_bin, stats in stats_men.items():
            data.append({'Attractiveness': attractiveness_bin, 'Gender': 'Men', 'Likes': stats['likes'], 'Matches': stats['matches']})
        for attractiveness_bin, stats in stats_women.items():
            data.append({'Attractiveness': attractiveness_bin, 'Gender': 'Women', 'Likes': stats['likes'], 'Matches': stats['matches']})

        df = pd.DataFrame(data)

        fig, ax = plt.subplots(1, 2, figsize=(15, 6))

        sns.barplot(x='Attractiveness', y='Likes', hue='Gender', data=df, ax=ax[0])
        ax[0].set_title('Number of Likes by Attractiveness')

        sns.barplot(x='Attractiveness', y='Matches', hue='Gender', data=df, ax=ax[1])
        
        ax[1].set_title('Number of Matches by Attractiveness')
        plt.suptitle('Distribution of likes/matches by attractiveness', fontsize=17);
        plt.savefig(path, dpi=500)
    
    
    def plot_functions(self, path='./plots/functions.png'):
        """
        Plots the attractiveness distribution functions for both genders.
        
        Args:
            path (str, optional): Path to save the plot. Defaults to './app/plots/functions.png'.
        """
        fig, ax = plt.subplots(1, 2, figsize=(12,5))

        x = np.arange(0.001, 1, 0.001)
        y = []
        for i in x:
            y.append(eval(self.men_formula.replace('x', f'{i}')))
        ax[0].plot(x, y, linewidth=2)
        ax[0].set_title('Men', fontsize=15)
        ax[0].set_xlabel('Attractiveness', fontsize=12)
        ax[0].set_ylabel('Probability to get like', fontsize=12)
        # ax[0].axhline(y = avg, color = 'r', linestyle = 'dashed') 
        # ax[0].text(0, 0.2, f'average = {avg}', color='red')

        x = np.arange(0, 1, 0.001)
        y = []
        for i in x:
            y.append(eval(self.women_formula.replace('x', f'{i}')))
        ax[1].plot(x, y, linewidth=2)
        ax[1].set_title('Women', fontsize=15)
        ax[1].set_xlabel('Attractiveness', fontsize=12)
        ax[1].set_ylabel('Probability to get like', fontsize=12)
        # ax[1].axhline(y = avg, color = 'r', linestyle = 'dashed')
        # ax[1].text(0, 0.5, f'average = {avg}', color='red')

        plt.suptitle('Attractivness distribution function', fontsize=17);
        plt.savefig(path, dpi=500)
            
    
## check     
# x = Simulation(1400, 600, 200, 200, 'x^5.67', 'x^1.22')
# x.simulate(1)
# x.plot_distributions(nbins=7)
# print(x.get_stats())
