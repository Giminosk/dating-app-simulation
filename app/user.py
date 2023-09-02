import numpy as np
import math
from typing import Union

class User:
    
    def __init__(self, gender: Union['M', 'W'], attractiveness: float, formula: str, is_premium: bool = False, num_swipes: int = 200):
        """
        Initializes a new User object.
        
        Args:
            gender (str): The gender of the user ('M' for male, 'W' for female).
            attractiveness (float): A measure of the user's attractiveness, ranging from 0 to 1.
            formula (str): The formula to calculate the attractiveness rate.
            is_premium (bool, optional): Indicates if the user has a premium account. Defaults to False.
            num_swipes (int, optional): The number of profiles the user can swipe per day. Defaults to 200.
        """
        self.gender = gender
        self.attractiveness = attractiveness
        self.attractiveness_rate = eval(formula.replace('x', f'{attractiveness}'))
        self.is_premium = is_premium
        self.num_swipes = num_swipes
        self.left_swipes = num_swipes
        self.given_likes = set()
        self.got_likes = set()
        self.num_likes = 0
        self.num_matches = 0
        
    def calculate_stats(self) -> None:
        """
        Calculates the number of likes and matches for the user.
        """
        self.num_likes = len(self.got_likes)
        self.num_matches = len(self.given_likes.intersection(self.got_likes))
        
    def refresh(self) -> None:
        """
        Resets the daily state of the user, including swipes and likes.
        """
        self.left_swipes = self.num_swipes
        self.given_likes = set()
        self.got_likes = set()
        self.num_likes = 0
        self.num_matches = 0
        
    def like(self, user: 'User') -> None:
        """
        Likes another user.
        
        Args:
            user (User): The user to like.
        """
        if user.gender == self.gender:
            return
        if self.left_swipes <= 0:
            return
        self.given_likes.add(user)
        user.got_likes.add(self)
        
    def get_stats(self) -> np.ndarray:
        """
        Gets the statistics of the user, including the number of likes and matches.
        
        Returns:
            np.ndarray: An array containing the number of likes and matches.
        """
        return np.array([self.num_likes, self.num_matches])
